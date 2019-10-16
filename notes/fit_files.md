# Fit Files

A few notes while parsing the Garmin fit files using the `fitparse`
python package.

Fit in general is a collection of data types with names to define the 
types of each piece of data.

# Example

From cycling file. The unique names are:

```
In [11]: names = set(m.name for m in l)               

In [12]: names             
Out[12]: 
{'activity',
 'device_info',
 'device_settings',
 'event',
 'file_creator',
 'file_id',
 'lap',
 'record',
 'session',
 'sport',
 'unknown_104',
 'unknown_113',
 'unknown_13',
 'unknown_140',
 'unknown_141',
 'unknown_147',
 'unknown_216',
 'unknown_22',
 'unknown_233',
 'unknown_79',
 'user_profile',
 'zones_target'}
```

A quick summary:

##  sport 

Information defining the sport:
```
<DataMessage: sport (#12) -- local mesg: #10, fields: [name: Trail Run, unknown_10: (None, 0, 0, None), unknown_4: 29, sport: running, sub_sport: trail, unknown_5: 1, unknown_6: 0, unknown_11: 1, unknown_12: None, unknown_13: 0]>
```

## activity 
```
[<DataMessage: activity (#34) -- local mesg: #9, fields: [timestamp: 2019-10-10 02:54:48, total_timer_time: 5414.037, local_timestamp: 2019-10-09 20:54:48, num_sessions: 1, type: manual, event: activity, event_type: stop, event_group: None, unknown_7: None]>
```

## session

Summary information

```
<DataMessage: session (#18) -- local mesg: #8, fields: [timestamp: 2019-10-10 02:54:48, start_time: 2019-10-10 01:24:22, start_position_lat: 485359025, start_position_long: -1333746292, total_elapsed_time: 5420.236, total_timer_time: 5414.037, total_distance: 11648.52, total_strides: 11, nec_lat: 485363314, nec_long: -1333645882, swc_lat: 484978553, swc_long: -1333868792, unknown_38: 485363314, unknown_39: -1333749008, avg_stroke_count: None, total_work: None, unknown_78: None, unknown_110: Trail Run, time_standing: None, avg_left_power_phase: (None, None, None, None), avg_left_power_phase_peak: (None, None, None, None), avg_right_power_phase: (None, None, None, None), avg_right_power_phase_peak: (None, None, None, None), avg_power_position: (None, None), max_power_position: (None, None), unknown_152: 0, message_index: 0, total_calories: 800, enhanced_avg_speed: 2.152, avg_speed: 2152, enhanced_max_speed: 3.854, max_speed: 3854, avg_power: None, max_power: None, total_ascent: 514, total_descent: 518, first_lap_index: 0, num_laps: 1, unknown_33: None, normalized_power: None, training_stress_score: None, intensity_factor: None, left_right_balance: None, avg_stroke_distance: None, pool_length: None, threshold_power: None, num_active_lengths: None, unknown_79: None, unknown_80: None, avg_vertical_oscillation: 105.0, avg_stance_time_percent: 39.23, avg_stance_time: 311.3, unknown_106: 0, unknown_107: None, unknown_108: None, stand_count: None, avg_vertical_ratio: 12.19, avg_stance_time_balance: 50.02, avg_step_length: 901.7, unknown_151: 0, unknown_157: None, unknown_158: None, event: lap, event_type: stop, sport: running, sub_sport: trail, avg_heart_rate: 129, max_heart_rate: 154, avg_running_cadence: 71, max_running_cadence: 113, total_training_effect: 2.4, event_group: None, trigger: activity_end, swim_stroke: None, pool_length_unit: None, avg_temperature: 20, max_temperature: 24, unknown_81: 0, avg_fractional_cadence: 0.0234375, max_fractional_cadence: 0.0, total_fractional_cycles: None, avg_left_torque_effectiveness: None, avg_right_torque_effectiveness: None, avg_left_pedal_smoothness: None, avg_right_pedal_smoothness: None, avg_combined_pedal_smoothness: None, unknown_109: None, avg_left_pco: None, avg_right_pco: None, avg_cadence_position: (None, None), max_cadence_position: (None, None), total_anaerobic_training_effect: 2.5, unknown_138: (7, 1), unknown_150: 15, unknown_184: 0]>
```

## record

Information about each instance

```
 <DataMessage: record (#20) -- local mesg: #13, fields: [timestamp: 2019-10-10 01:24:22, position_lat: None, position_long: None, distance: 0.0, enhanced_altitude: 1527.4, altitude: 10137, unknown_87: 0, unknown_88: 100, heart_rate: 88, cadence: 0, temperature: 24, fractional_cadence: 0.0]>
```

The results don't always have the same data
```
<DataMessage: record (#20) -- local mesg: #0, fields: [timestamp: 2019-10-10 01:29:10, position_lat: 485296265, position_long: -1333711149, distance: 761.07, enhanced_altitude: 1572.8000000000002, altitude: 10364, enhanced_speed: 2.715, speed: 2715, vertical_oscillation: 110.2, stance_time_percent: 38.25, stance_time: 291.0, vertical_ratio: 10.53, stance_time_balance: 50.18, step_length: 1015.0, unknown_87: 0, unknown_88: 300, heart_rate: 145, cadence: 78, temperature: 19, activity_type: running, fractional_cadence: 0.5]>
```
