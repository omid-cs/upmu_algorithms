algorithms = {
  'frequency' :        { 'path'    : 'cab.frequency.Frequency',
                         'deps'    : ['phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['1-SEC', 'C37'] },

  'angle_difference' : { 'path'    : 'cab.angle_difference.Angle_Difference',
                         'deps'    : ['angle1', 'angle2'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['ANGLE-DIFFERENCE'] },

  'rpfp'             : { 'path'    : 'saa.rpfp.RPFP',
                         'deps'    : ['voltage_phase', 'current_phase', 'voltage_mag', 'current_mag'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['REACTIVE-POWER', 'FUNDAMENTAL-POWER'] },

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
                        'outputs' : ['CLEAN'] },
                         
  'sequence_ref'    : { 'path'    : 'alu.sequence.Sequence',
                        'deps'    : ['M1', 'M2', 'M3', 'A1', 'A2', 'A3','Reference_Angle'],
                        'params'  : ['section', 'name'],
                        'outputs' : ['ZERO_SEQ_ANG', 'ZERO_SEQ_MAG',
                                     'POSITIVE_SEQ_ANG', 'POSITIVE_SEQ_MAG',
                                     'NEGATIVE_SEQ_ANG', 'NEGATIVE_SEQ_MAG',
                                     'UNBALANCE_NEG_SEQ', 'UNBALANCE_ZERO_SEQ'] },

  'filter'          : { 'path'    : 'cab.filter.Filter',
                        'deps'    : ['UNFILTERED'],
                        'params'  : ['section', 'name', 'units', 'window_time', 'availability_threshold'],
                        'outputs' : ['FILTERED'] }
}
locations = ['LBNL', 'UCB', 'PSL', 'TVA', 'RPU']
