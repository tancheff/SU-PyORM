--[p_ata_sb_wifi_analytics].[vwt_bulk]
--HDFS: prod_customer360.vw_lifemote_wifianalytics_bulk
with last_analysis_max as (
    SELECT MAX(CAST(last_analysis AS DATE)) as maxi
    FROM p_ata_sb_wifi_analytics.vwt_bulk
),
-- temp Openrowset, change when view is fixed
vwm_subscription_h as(
    select *
    from OPENROWSET(
            BULK 'https://atsaprod001.blob.core.windows.net/staging/dwh_mv_sfbase/vwm_subscription_h/processed/**',
            FORMAT = 'PARQUET'
        ) r
),
coverage_agg AS (
    SELECT mac_address,
        SUM(wifi_coverage_numeric) AS bad_coverage_days,
        SUM(bad_placement_numeric) AS bad_placement_days,
        SUM(poor_legacy_numeric) AS poor_legacy_device_days,
        SUM(poor_memory_status_numeric) AS poor_memory_days,
        SUM(split_ssid_numeric) AS split_ssid_days,
        SUM(dsl_bottleneck_numeric) AS dsl_dl_bottleneck_days,
        SUM(dsl_bottleneck) AS dsl_dl_bottleneck_minutes,
        SUM(ssid_mesh_active) as ssid_mesh_active_days,
        dsl_dl_median_bitrate,
        SUM(bad_wifi_qoe_numeric) AS bad_wifi_qoe_days,      -- ADDED
        bad_wifi_qoe                                         -- ADDED
    FROM (
            SELECT device_id AS mac_address,
                last_analysis,
                MAX(CASE WHEN wifi_coverage_status = 'POOR' THEN 1 ELSE 0 END) AS wifi_coverage_numeric,
                MAX(CASE WHEN Poor_GW_Status = 'POOR' THEN 1 ELSE 0 END) AS bad_placement_numeric,
                MAX(CASE WHEN legacy_status = 'POOR' THEN 1 ELSE 0 END) AS poor_legacy_numeric,
                MAX(CASE WHEN memory_status = 'POOR' THEN 1 ELSE 0 END) AS poor_memory_status_numeric,
                MAX(CASE WHEN ssid_status = 'SPLIT' THEN 1 ELSE 0 END) AS split_ssid_numeric,
                MAX(CASE WHEN dsl_download_bottleneck_count > 0 THEN 1 ELSE 0 END) AS dsl_bottleneck_numeric,
                SUM(dsl_download_bottleneck_count) AS dsl_bottleneck,
                MAX(max_dsl_down_attainable) AS max_dsl_down_attainable,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY MAX(max_dsl_down_attainable))
                    OVER (partition by device_id) as dsl_dl_median_bitrate,
                MAX(CASE WHEN (main_ssid_count_24 = 1 OR main_ssid_count_5 = 1)
                    AND coalesce(data_usage_24,0) = 0
                    AND coalesce(data_usage_5,0) = 0 then 1 ELSE 0 END) as ssid_mesh_active,
                MAX(CASE WHEN wifi_qoe_status IN ('POOR', 'MID') THEN 1 ELSE 0 END) AS bad_wifi_qoe_numeric, -- ADDED
                wifi_qoe_status AS bad_wifi_qoe                                                              -- ADDED
            FROM p_ata_sb_wifi_analytics.vwt_bulk
            WHERE cast(last_analysis as DATE) > (select DATEADD(day, -30, CONVERT(date, maxi)) from last_analysis_max)
            GROUP BY device_id, last_analysis,
                        wifi_qoe_status, bad_wifi_qoe           -- ADDED
        ) tmp
    GROUP BY mac_address, dsl_dl_median_bitrate
),
device_calc AS (
    SELECT DISTINCT device.id AS hdm_device_id,
        replace(device.serialnumber, '"', '') AS serialnumber,
        replace(device.manufacturer, '"', '') AS manufacturer,
        replace(device.subscriberid, '"', '') AS subscriberid,
        coverage_agg.mac_address,
        replace(device.product_class, '"', '') AS product_class,
        coverage_agg.bad_coverage_days,
        coverage_agg.bad_placement_days,
        coverage_agg.poor_legacy_device_days,
        coverage_agg.poor_memory_days,
        coverage_agg.split_ssid_days,
        coverage_agg.dsl_dl_bottleneck_days,
        coverage_agg.dsl_dl_bottleneck_minutes,
        coverage_agg.ssid_mesh_active_days,
        coverage_agg.bad_wifi_qoe,      -- ADDED
        coverage_agg.bad_wifi_qoe_days,  -- ADDED
        CAST(
            ROUND(coverage_agg.dsl_dl_median_bitrate, 4) AS DECIMAL(15, 4)) AS dsl_dl_median_bitrate
    FROM coverage_agg
        INNER JOIN p_ata_sb_dwh_sv_hdm.usertags_h usertags
            ON replace(upper(usertags.value_), '"', '') = coverage_agg.mac_address
            AND Getdate() BETWEEN usertags.rec_start AND usertags.rec_end
            AND usertags.rec_stat = 'A'
        INNER JOIN p_ata_sb_dwh_sv_hdm.device_h device
            ON device.id = usertags.device_id
            AND Getdate() BETWEEN device.rec_start AND device.rec_end
            AND device.rec_stat = 'A'
),
mesh AS (
    SELECT subscription_key,
        COUNT(DISTINCT device_id) AS mesh_ap_cnt,
        MAX(device_used_days_of_last_60_cnt) AS mesh_used_days_of_last_60_cnt
    FROM p_ata_sb_dwh_mv_sfbase.vwf_subscription_hdm
    WHERE manufacturer IN ('TP-Link', 'Arcadyan', 'ZYXEL')
        AND last_contact_dat >= DATEADD(day, -60, GETDATE())
        AND is_gateway = 0
    GROUP BY subscription_key
)


SELECT DISTINCT device_calc.hdm_device_id,
    device_calc.manufacturer,
    device_calc.subscriberid,
    device_calc.product_class,
    device_calc.bad_coverage_days,
    device_calc.bad_placement_days,
    device_calc.poor_legacy_device_days,
    device_calc.poor_memory_days,
    device_calc.split_ssid_days,
    device_calc.dsl_dl_bottleneck_days,
    device_calc.dsl_dl_bottleneck_minutes,
    device_calc.bad_wifi_qoe,        -- ADDED
    device_calc.bad_wifi_qoe_days,   -- ADDED
    CASE WHEN COALESCE(mesh.mesh_ap_cnt, 0) > 0 THEN device_calc.ssid_mesh_active_days ELSE 0 END AS modem_wifi_active_despite_mesh_days,
    device_calc.dsl_dl_median_bitrate,
    subs.subscription_key,
    COALESCE(bulks.ap_status, -1) AS ap_status,
    bulks.dsl_status,
    bulks.last_analysis,
    COALESCE(bulks.max_dsl_down, -1) AS max_dsl_down,
    COALESCE(bulks.max_dsl_down_attainable, -1) AS max_dsl_down_attainable,
    COALESCE(bulks.max_dsl_up_attainable, -1) AS max_dsl_up_attainable,
    COALESCE(bulks.min_dsl_down, -1) AS min_dsl_down,
    COALESCE(bulks.number_of_stations, -1) AS number_of_stations,
    COALESCE(bulks.poor_active_sample_count, -1) AS poor_active_sample_count,
    COALESCE(bulks.poor_client_coverage_status_count, -1) AS poor_client_coverage_status_count,
    bulks.poor_gw_status,
    COALESCE(bulks.poor_qoe_samples, -1) AS poor_qoe_samples,
    COALESCE(bulks.poor_sample_count, -1) AS poor_sample_count,
    COALESCE(bulks.reboots, -1) AS reboots,
    bulks.repeater_status,
    COALESCE(bulks.uptime_in_minutes, -1) AS uptime_in_minutes,
    bulks.wifi_coverage_status,
    COALESCE(mesh.mesh_ap_cnt, 0) as mesh_ap_cnt,
    CASE
        WHEN COALESCE(mesh.mesh_ap_cnt, 0) > 0 THEN 'Y'
        ELSE 'N'
    END AS mesh_active_yn,
    coalesce(mesh.mesh_used_days_of_last_60_cnt, 0) as mesh_used_days_of_last_60_cnt,
    year(last_analysis_max.maxi) as year,
    month(last_analysis_max.maxi) as month,
    day(last_analysis_max.maxi) as day
FROM device_calc
    CROSS JOIN last_analysis_max
    INNER JOIN vwm_subscription_h subs
        ON CONCAT('43',LTRIM(SUBSTRING(device_calc.subscriberid, 2, 20))) = subs.phone_num
--         AND Getdate() BETWEEN subs.rec_start AND subs.rec_end    -- REMOVED
--         AND subs.rec_stat = 'A'                                  -- REMOVED
    LEFT OUTER JOIN mesh
        ON subs.subscription_key = mesh.subscription_key
    INNER JOIN p_ata_sb_wifi_analytics.vwt_bulk bulks
        ON device_calc.mac_address = bulks.device_id
    WHERE CAST(bulks.last_analysis AS DATE) = last_analysis_max.maxi