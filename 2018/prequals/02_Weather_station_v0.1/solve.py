# coding=utf-8


func = """
/ (fcn) fcn.0000049c 564
|   fcn.0000049c ();
|           ; CALL XREF from 0x000000b2 (entry0)
|           ; CALL XREF from 0x0000049c (fcn.0000049c)
|           0x0000049c      7894           sei
|           0x0000049e      84b5           in r24, 0x24                ; '$' ; IO TCNT2: Timer/Counter2 (8 bits).
|           0x000004a0      8260           ori r24, 0x02
|           0x000004a2      84bd           out 0x24, r24               ; '$' ; IO TCNT2: Timer/Counter2 (8 bits).
|           0x000004a4      84b5           in r24, 0x24                ; '$' ; IO TCNT2: Timer/Counter2 (8 bits).
|           0x000004a6      8160           ori r24, 0x01
|           0x000004a8      84bd           out 0x24, r24               ; '$' ; IO TCNT2: Timer/Counter2 (8 bits).
|           0x000004aa      85b5           in r24, 0x25                ; '%' ; IO TCCR2: Timer/Counter2 Control Register (8 bits).
|           0x000004ac      8260           ori r24, 0x02
|           0x000004ae      85bd           out 0x25, r24               ; '%' ; IO TCCR2: Timer/Counter2 Control Register (8 bits).
|           0x000004b0      85b5           in r24, 0x25                ; '%' ; IO TCCR2: Timer/Counter2 Control Register (8 bits).
|           0x000004b2      8160           ori r24, 0x01
|           0x000004b4      85bd           out 0x25, r24               ; '%' ; IO TCCR2: Timer/Counter2 Control Register (8 bits).
|           0x000004b6      80916e00       lds r24, 0x6e               ; 'n'
|           0x000004ba      8160           ori r24, 0x01
|           0x000004bc      80936e00       sts 0x6e, r24               ; 'n'
|           0x000004c0      10928100       sts 0x81, r1
|           0x000004c4      80918100       lds r24, 0x81
|           0x000004c8      8260           ori r24, 0x02
|           0x000004ca      80938100       sts 0x81, r24
|           0x000004ce      80918100       lds r24, 0x81
|           0x000004d2      8160           ori r24, 0x01
|           0x000004d4      80938100       sts 0x81, r24
|           0x000004d8      80918000       lds r24, 0x80
|           0x000004dc      8160           ori r24, 0x01
|           0x000004de      80938000       sts 0x80, r24
|           0x000004e2      8091b100       lds r24, 0xb1
|           0x000004e6      8460           ori r24, 0x04
|           0x000004e8      8093b100       sts 0xb1, r24
|           0x000004ec      8091b000       lds r24, 0xb0
|           0x000004f0      8160           ori r24, 0x01
|           0x000004f2      8093b000       sts 0xb0, r24
|           0x000004f6      80917a00       lds r24, 0x7a               ; 'z'
|           0x000004fa      8460           ori r24, 0x04
|           0x000004fc      80937a00       sts 0x7a, r24               ; 'z'
|           0x00000500      80917a00       lds r24, 0x7a               ; 'z'
|           0x00000504      8260           ori r24, 0x02
|           0x00000506      80937a00       sts 0x7a, r24               ; 'z'
|           0x0000050a      80917a00       lds r24, 0x7a               ; 'z'
|           0x0000050e      8160           ori r24, 0x01
|           0x00000510      80937a00       sts 0x7a, r24               ; 'z'
|           0x00000514      80917a00       lds r24, 0x7a               ; 'z'
|           0x00000518      8068           ori r24, 0x80
|           0x0000051a      80937a00       sts 0x7a, r24               ; 'z'
|           0x0000051e      1092c100       sts 0xc1, r1
|           0x00000522      e0916b01       lds r30, 0x16b
|           0x00000526      f0916c01       lds r31, 0x16c
|           0x0000052a      82e0           ldi r24, 0x02
|           0x0000052c      8083           std z+0, r24
|           0x0000052e      e0916701       lds r30, 0x167
|           0x00000532      f0916801       lds r31, 0x168
|           0x00000536      1082           std z+0, r1
|           0x00000538      e0916901       lds r30, 0x169
|           0x0000053c      f0916a01       lds r31, 0x16a
|           0x00000540      8fec           ldi r24, 0xcf
|           0x00000542      8083           std z+0, r24
|           0x00000544      10927301       sts 0x173, r1
|           0x00000548      e0916f01       lds r30, 0x16f
|           0x0000054c      f0917001       lds r31, 0x170
|           0x00000550      86e0           ldi r24, 0x06
|           0x00000552      8083           std z+0, r24
|           0x00000554      e0916d01       lds r30, 0x16d
|           0x00000558      f0916e01       lds r31, 0x16e
|           0x0000055c      8081           ld r24, z
|           0x0000055e      8061           ori r24, 0x10
|           0x00000560      8083           std z+0, r24
|           0x00000562      e0916d01       lds r30, 0x16d
|           0x00000566      f0916e01       lds r31, 0x16e
|           0x0000056a      8081           ld r24, z
|           0x0000056c      8860           ori r24, 0x08
|           0x0000056e      8083           std z+0, r24
|           0x00000570      e0916d01       lds r30, 0x16d
|           0x00000574      f0916e01       lds r31, 0x16e
|           0x00000578      8081           ld r24, z
|           0x0000057a      8068           ori r24, 0x80
|           0x0000057c      8083           std z+0, r24
|           0x0000057e      e0916d01       lds r30, 0x16d
|           0x00000582      f0916e01       lds r31, 0x16e
|           0x00000586      8081           ld r24, z
|           0x00000588      8f7d           andi r24, 0xdf
|           0x0000058a      8083           std z+0, r24
|           0x0000058c      c1e0           ldi r28, 0x01
|           0x0000058e      d0e0           ldi r29, 0x00
|           ; JMP XREF from 0x000006ce (fcn.0000049c)
|       .-> 0x00000590      80915901       lds r24, 0x159
|       :   0x00000594      90915a01       lds r25, 0x15a
|       :   0x00000598      892b           or r24, r25
|      ,==< 0x0000059a      09f0           breq 0x59e
|     ,===< 0x0000059c      6fc0           rjmp 0x67c
|     ||:   ; JMP XREF from 0x0000059a (fcn.0000049c)
|     |`--> 0x0000059e      82e1           ldi r24, 0x12
|     | :   0x000005a0      91e0           ldi r25, 0x01
|     | :   0x000005a2      0e949801       call fcn.00000330
|     | :   0x000005a6      88e2           ldi r24, 0x28               ; '('
|     | :   0x000005a8      91e0           ldi r25, 0x01
|     | :   0x000005aa      0e949801       call fcn.00000330
|     | :   0x000005ae      8be5           ldi r24, 0x5b               ; '['
|     | :   0x000005b0      91e0           ldi r25, 0x01
|     | :   0x000005b2      0e943d01       call fcn.0000027a
|     | :   0x000005b6      0e948e01       call fcn.0000031c
|     | :   0x000005ba      8734           cpi r24, 0x47
|     | :   0x000005bc      9105           cpc r25, r1
|     |,==< 0x000005be      09f0           breq 0x5c2
|    ,====< 0x000005c0      59c0           rjmp 0x674
|    |||:   ; JMP XREF from 0x000005be (fcn.0000049c)
|    ||`--> 0x000005c2      0e948e01       call fcn.0000031c
|    || :   0x000005c6      8834           cpi r24, 0x48
|    || :   0x000005c8      9105           cpc r25, r1
|    ||,==< 0x000005ca      09f0           breq 0x5ce
|   ,=====< 0x000005cc      53c0           rjmp 0x674
|   ||||:   ; JMP XREF from 0x000005ca (fcn.0000049c)
|   |||`--> 0x000005ce      0e948e01       call fcn.0000031c
|   ||| :   0x000005d2      c197           sbiw r24, 0x31              ; '1'
|   |||,==< 0x000005d4      09f0           breq 0x5d8
|  ,======< 0x000005d6      4ec0           rjmp 0x674
|  |||||:   ; JMP XREF from 0x000005d4 (fcn.0000049c)
|  ||||`--> 0x000005d8      0e948e01       call fcn.0000031c
|  |||| :   0x000005dc      c897           sbiw r24, 0x38              ; '8'
|  ||||,==< 0x000005de      09f0           breq 0x5e2
| ,=======< 0x000005e0      49c0           rjmp 0x674
| ||||||:   ; JMP XREF from 0x000005de (fcn.0000049c)
| |||||`--> 0x000005e2      0e948e01       call fcn.0000031c
| ||||| :   0x000005e6      8b37           cpi r24, 0x7b
| ||||| :   0x000005e8      9105           cpc r25, r1
| |||||,==< 0x000005ea      09f0           breq 0x5ee
| ========< 0x000005ec      43c0           rjmp 0x674
| ||||||:   ; JMP XREF from 0x000005ea (fcn.0000049c)
| |||||`--> 0x000005ee      0e948e01       call fcn.0000031c
| ||||| :   0x000005f2      8134           cpi r24, 0x41
| ||||| :   0x000005f4      9105           cpc r25, r1
| |||||,==< 0x000005f6      f1f5           brne 0x674
| ||||||:   0x000005f8      0e948e01       call fcn.0000031c
| ||||||:   0x000005fc      8635           cpi r24, 0x56
| ||||||:   0x000005fe      9105           cpc r25, r1
| ========< 0x00000600      c9f5           brne 0x674
| ||||||:   0x00000602      0e948e01       call fcn.0000031c
| ||||||:   0x00000606      8235           cpi r24, 0x52
| ||||||:   0x00000608      9105           cpc r25, r1
| ========< 0x0000060a      a1f5           brne 0x674
| ||||||:   0x0000060c      0e948e01       call fcn.0000031c
| ||||||:   0x00000610      8f35           cpi r24, 0x5f
| ||||||:   0x00000612      9105           cpc r25, r1
| ========< 0x00000614      79f5           brne 0x674
| ||||||:   0x00000616      0e948e01       call fcn.0000031c
| ||||||:   0x0000061a      8335           cpi r24, 0x53
| ||||||:   0x0000061c      9105           cpc r25, r1
| ========< 0x0000061e      51f5           brne 0x674
| ||||||:   0x00000620      0e948e01       call fcn.0000031c
| ||||||:   0x00000624      8437           cpi r24, 0x74
| ||||||:   0x00000626      9105           cpc r25, r1
| ========< 0x00000628      29f5           brne 0x674
| ||||||:   0x0000062a      0e948e01       call fcn.0000031c
| ||||||:   0x0000062e      c497           sbiw r24, 0x34              ; '4'
| ========< 0x00000630      09f5           brne 0x674
| ||||||:   0x00000632      0e948e01       call fcn.0000031c
| ||||||:   0x00000636      8437           cpi r24, 0x74
| ||||||:   0x00000638      9105           cpc r25, r1
| ========< 0x0000063a      e1f4           brne 0x674
| ||||||:   0x0000063c      0e948e01       call fcn.0000031c
| ||||||:   0x00000640      8197           sbiw r24, 0x21              ; '!'
| ========< 0x00000642      c1f4           brne 0x674
| ||||||:   0x00000644      0e948e01       call fcn.0000031c
| ||||||:   0x00000648      8f36           cpi r24, 0x6f
| ||||||:   0x0000064a      9105           cpc r25, r1
| ========< 0x0000064c      99f4           brne 0x674
| ||||||:   0x0000064e      0e948e01       call fcn.0000031c
| ||||||:   0x00000652      8e36           cpi r24, 0x6e
| ||||||:   0x00000654      9105           cpc r25, r1
| ========< 0x00000656      71f4           brne 0x674
| ||||||:   0x00000658      0e948e01       call fcn.0000031c
| ||||||:   0x0000065c      8d37           cpi r24, 0x7d
| ||||||:   0x0000065e      9105           cpc r25, r1
| ========< 0x00000660      49f4           brne 0x674
| ||||||:   0x00000662      84e3           ldi r24, 0x34               ; '4'
| ||||||:   0x00000664      91e0           ldi r25, 0x01
| ||||||:   0x00000666      0e949801       call fcn.00000330
| ||||||:   0x0000066a      d0935a01       sts 0x15a, r29
| ||||||:   0x0000066e      c0935901       sts 0x159, r28
| ========< 0x00000672      2bc0           rjmp 0x6ca
| ||||||:   ; XREFS: JMP 0x000005c0  JMP 0x000005cc  JMP 0x000005d6  JMP 0x000005e0  JMP 0x000005ec  
| ||||||:   ; XREFS: JMP 0x000005f6  JMP 0x00000600  JMP 0x0000060a  JMP 0x00000614  JMP 0x0000061e  
| ||||||:   ; XREFS: JMP 0x00000628  JMP 0x00000630  JMP 0x0000063a  JMP 0x00000642  JMP 0x0000064c  
| ||||||:   ; XREFS: JMP 0x00000656  JMP 0x00000660  
| ````-`--> 0x00000674      8fe3           ldi r24, 0x3f               ; '?'
|     | :   0x00000676      91e0           ldi r25, 0x01
|     | :   0x00000678      0e949801       call fcn.00000330
|     | :   ; JMP XREF from 0x0000059c (fcn.0000049c)
|     `---> 0x0000067c      0e946901       call fcn.000002d2
|       :   0x00000680      4b01           movw r8, r22
|       :   0x00000682      5c01           movw r10, r24
|       :   0x00000684      84ef           ldi r24, 0xf4
|       :   0x00000686      c82e           mov r12, r24
|       :   0x00000688      dd24           clr r13
|       :   0x0000068a      d394           inc r13
|       :   0x0000068c      e12c           mov r14, r1
|       :   0x0000068e      f12c           mov r15, r1
|       :   ; JMP XREF from 0x000006c8 (fcn.0000049c)
|      .--> 0x00000690      0e946901       call fcn.000002d2
|      ::   0x00000694      dc01           movw r26, r24
|      ::   0x00000696      cb01           movw r24, r22
|      ::   0x00000698      8819           sub r24, r8
|      ::   0x0000069a      9909           sbc r25, r9
|      ::   0x0000069c      aa09           sbc r26, r10
|      ::   0x0000069e      bb09           sbc r27, r11
|      ::   0x000006a0      883e           cpi r24, 0xe8
|      ::   0x000006a2      9340           sbci r25, 0x03
|      ::   0x000006a4      a105           cpc r26, r1
|      ::   0x000006a6      b105           cpc r27, r1
|     ,===< 0x000006a8      58f0           brcs 0x6c0
|     |::   0x000006aa      21e0           ldi r18, 0x01
|     |::   0x000006ac      c21a           sub r12, r18
|     |::   0x000006ae      d108           sbc r13, r1
|     |::   0x000006b0      e108           sbc r14, r1
|     |::   0x000006b2      f108           sbc r15, r1
|     |::   0x000006b4      88ee           ldi r24, 0xe8
|     |::   0x000006b6      880e           add r8, r24
|     |::   0x000006b8      83e0           ldi r24, 0x03
|     |::   0x000006ba      981e           adc r9, r24
|     |::   0x000006bc      a11c           adc r10, r1
|     |::   0x000006be      b11c           adc r11, r1
|     |::   ; JMP XREF from 0x000006a8 (fcn.0000049c)
|     `---> 0x000006c0      c114           cp r12, r1
|      ::   0x000006c2      d104           cpc r13, r1
|      ::   0x000006c4      e104           cpc r14, r1
|      ::   0x000006c6      f104           cpc r15, r1
|      `==< 0x000006c8      19f7           brne 0x690
|       :   ; JMP XREF from 0x00000672 (fcn.0000049c)
| --------> 0x000006ca      0e945f01       call fcn.000002be
\       `=< 0x000006ce      60cf           rjmp 0x590
""".splitlines()
print("".join([func[i+1].split(", 0x")[1].split(" ")[0].decode("hex") if "call fcn.0000031c" in l else "" for i, l in enumerate(func)]))
