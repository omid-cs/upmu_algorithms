algorithms = {
  'frequency' :        { 'path'    : 'cab.frequency.Frequency',
                         'deps'    : ['phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['1-SEC', 'C37'] },

  'angle_difference' : { 'path'    : 'cab.angle_difference.Angle_Difference',
                         'deps'    : ['angle1', 'angle2'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['ANGLE-DIFFERENCE'] },

  'fundamental_power': { 'path'    : 'cab.fundamental_power.Fundamental_Power',
                         'deps'    : ['voltage_phase', 'current_phase', 'dpf'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['FUNDAMENTAL_POWER'] },

  'reactive_power'   : { 'path'    : 'cab.reactive_power.Reactive_Power',
                         'deps'    : ['voltage_phase', 'current_phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['REACTIVE_POWER'] },

   'dpf'             : { 'path'    : 'cab.dpf.DPF',
                         'deps'    : ['voltage_phase', 'current_phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['DPF'] },

   'sequence'        : { 'path'    : 'alu.sequence.Sequence',
                         'deps'    : ['M1', 'M2', 'M3', 'A1', 'A2', 'A3'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['ZERO_SEQ_ANG', 'ZERO_SEQ_MAG',
                                      'POSITIVE_SEQ_ANG', 'POSITIVE_SEQ_MAG',
                                      'NEGATIVE_SEQ_ANG', 'NEGATIVE_SEQ_ANG',
                                      'UNBALANCE_NEG_SEQ', 'UNBALANCE_ZERO_SEQ'] },
   'clean'           : { 'path'    : 'cab.clean.Clean',
                         'deps'    : ['raw'],
                         'params'  : ['section', 'name', 'stream_type'],
                         'outputs' : ['CLEAN'] }
}
