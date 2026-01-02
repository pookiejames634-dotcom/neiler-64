; Neiler-OS Bootloader
; Stage 1: Boot sector loaded by BIOS
; Loads Stage 2 bootloader and kernel

BITS 16
ORG 0x7C00                    ; BIOS loads bootloader at 0x7C00

; Boot sector entry point
start:
    cli                       ; Disable interrupts
    xor ax, ax               ; Clear AX
    mov ds, ax               ; Set DS = 0
    mov es, ax               ; Set ES = 0
    mov ss, ax               ; Set SS = 0
    mov sp, 0x7C00           ; Stack grows down from bootloader
    sti                      ; Enable interrupts

    ; Print boot message
    mov si, msg_boot
    call print_string

    ; Load Stage 2 bootloader from disk
    mov si, msg_loading
    call print_string

    ; Reset disk system
    xor ah, ah
    xor dl, dl
    int 0x13
    jc disk_error

    ; Load Stage 2 (sectors 2-10 to 0x7E00)
    mov ah, 0x02             ; Read sectors function
    mov al, 9                ; Number of sectors to read
    mov ch, 0                ; Cylinder 0
    mov cl, 2                ; Start from sector 2
    mov dh, 0                ; Head 0
    mov dl, 0                ; Drive 0 (boot drive)
    mov bx, 0x7E00           ; Load to 0x7E00
    int 0x13
    jc disk_error

    ; Jump to Stage 2
    jmp 0x0000:0x7E00

disk_error:
    mov si, msg_disk_error
    call print_string
    hlt

; Print string function (SI = string address)
print_string:
    pusha
.loop:
    lodsb                    ; Load byte from SI into AL
    test al, al              ; Check for null terminator
    jz .done
    mov ah, 0x0E             ; BIOS teletype function
    mov bh, 0                ; Page 0
    int 0x10                 ; BIOS video interrupt
    jmp .loop
.done:
    popa
    ret

; Boot messages
msg_boot:        db 'Neiler-OS Bootloader v1.0', 13, 10, 0
msg_loading:     db 'Loading kernel...', 13, 10, 0
msg_disk_error:  db 'DISK ERROR!', 13, 10, 0

; Pad to 510 bytes and add boot signature
times 510-($-$$) db 0
dw 0xAA55                    ; Boot signature

; ========================================
; Stage 2 Bootloader
; ========================================
stage2_start:
    ; Print Stage 2 message
    mov si, msg_stage2
    call print_string

    ; Enable A20 line (required for > 1MB memory access)
    call enable_a20

    ; Load GDT (Global Descriptor Table)
    cli
    lgdt [gdt_descriptor]

    ; Switch to protected mode
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; Far jump to 32-bit code segment
    jmp CODE_SEG:protected_mode_start

enable_a20:
    in al, 0x92
    or al, 2
    out 0x92, al
    ret

msg_stage2: db 'Stage 2 loaded', 13, 10, 0

; GDT Definition
gdt_start:
    ; Null descriptor
    dq 0

gdt_code:
    ; Code segment descriptor
    dw 0xFFFF        ; Limit (low)
    dw 0x0000        ; Base (low)
    db 0x00          ; Base (middle)
    db 10011010b     ; Access byte
    db 11001111b     ; Flags + Limit (high)
    db 0x00          ; Base (high)

gdt_data:
    ; Data segment descriptor
    dw 0xFFFF        ; Limit (low)
    dw 0x0000        ; Base (low)
    db 0x00          ; Base (middle)
    db 10010010b     ; Access byte
    db 11001111b     ; Flags + Limit (high)
    db 0x00          ; Base (high)

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1  ; Size
    dd gdt_start                 ; Offset

CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start

; ========================================
; 32-bit Protected Mode
; ========================================
BITS 32
protected_mode_start:
    ; Set up segment registers
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x90000     ; Set up stack

    ; Print 32-bit mode message
    mov esi, msg_protected
    call print_string_pm

    ; Load kernel from disk to 0x100000 (1MB)
    ; (Simplified - real implementation would use BIOS INT 13h extensions)

    ; Jump to kernel entry point
    call 0x100000

    ; Should never return
    jmp $

; 32-bit print function (ESI = string)
print_string_pm:
    pusha
    mov edx, 0xB8000         ; VGA text mode buffer
.loop:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0F             ; White on black
    mov [edx], ax
    add edx, 2
    jmp .loop
.done:
    popa
    ret

msg_protected: db 'Protected mode enabled. Starting kernel...', 0

; Pad Stage 2
times 4096-($-stage2_start) db 0
