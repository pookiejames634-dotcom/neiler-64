; Hello World for Neiler-8
; Prints "HELLO WORLD" to terminal (port 0x01)

START:
    MOV X, 0            ; Start at beginning of string

LOOP:
    LOAD A, [X]         ; Load character
    CMP A, 0            ; Check for null terminator
    JZ END              ; If zero, we're done
    OUT 0x01, A         ; Output character to terminal
    INC X               ; Next character
    JMP LOOP            ; Repeat

END:
    HLT                 ; Halt CPU

; String data (would be at specific address in real impl)
; "HELLO WORLD" = 72 69 76 76 79 32 87 79 82 76 68 00
