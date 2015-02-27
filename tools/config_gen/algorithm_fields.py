alg_list = ['frequency', 'phase_difference']

settings = {
  'frequency' :        { 'path'    : 'cab.frequency.Frequency',
                         'deps'    : ['phase'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['1-Sec', 'C37'] },

  'phase_difference' : { 'path'    : 'cab.phase_difference.Phase_Difference',
                         'deps'    : ['phase1', 'phase2'],
                         'params'  : ['section', 'name'],
                         'outputs' : ['phase_difference'] }
}
