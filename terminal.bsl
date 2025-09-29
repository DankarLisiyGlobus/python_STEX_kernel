PRINT START TERMINAL
INPUT com >>>

DEF <help_def>::PRINT Это справка,,PRINT Это конец справки

IF /@com == 'help'/:CALL help_def

PRINTVAR com

PRINT SLEEP TERMINAL
create_task waiting wait.bsl
sleep_task 0

PRINT CONTIUNE TERMINAL

PRINT END TERMINAL