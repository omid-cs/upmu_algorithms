algorithms = {
  'frequency' :        { 'path'    : 'cab.frequency.Frequency',
                         'deps'    : ['phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['1-Sec', 'C37'] },

  'phase_difference' : { 'path'    : 'cab.phase_difference.Phase_Difference',
                         'deps'    : ['phase1', 'phase2'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['phase_difference'] },

  'fundamental_power': { 'path'    : 'cab.fundamental_power.Rundamental_Power',
                         'deps'    : ['voltage_phase', 'current_phase', 'dpf'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['Fundamental_Power'] },

  'reactive_power'   : { 'path'    : 'cab.reactive_power.Reactive_Power',
                         'deps'    : ['voltage_phase', 'current_phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['Reactive_Power'] },

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
}
