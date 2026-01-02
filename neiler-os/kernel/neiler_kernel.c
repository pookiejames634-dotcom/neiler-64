/**
 * Neiler-OS Kernel
 *
 * A modern, developer-focused operating system kernel
 * Designed for the Neiler-64 computer architecture
 *
 * Features:
 * - Preemptive multitasking
 * - Virtual memory management
 * - Advanced filesystem support
 * - Hardware abstraction layer
 * - Developer-friendly APIs
 */

#include <stdint.h>
#include <stdbool.h>
#include "neiler_kernel.h"
#include "neiler_mm.h"
#include "neiler_proc.h"
#include "neiler_fs.h"
#include "neiler_dev.h"

// Kernel version
#define NEILER_OS_VERSION_MAJOR 1
#define NEILER_OS_VERSION_MINOR 0
#define NEILER_OS_VERSION_PATCH 0
#define NEILER_OS_CODENAME "Developer Edition"

// Kernel state
typedef struct {
    uint32_t uptime;              // System uptime in ticks
    uint32_t total_memory;        // Total RAM in bytes
    uint32_t free_memory;         // Available RAM
    uint32_t process_count;       // Number of running processes
    bool initialized;             // Kernel initialization complete
    char hostname[256];           // System hostname
} kernel_state_t;

static kernel_state_t kernel_state = {0};

/**
 * Kernel initialization
 */
void kernel_init(void) {
    // Print boot banner
    kernel_printf("\n");
    kernel_printf("========================================\n");
    kernel_printf("      Neiler-OS v%d.%d.%d\n",
        NEILER_OS_VERSION_MAJOR,
        NEILER_OS_VERSION_MINOR,
        NEILER_OS_VERSION_PATCH);
    kernel_printf("      %s\n", NEILER_OS_CODENAME);
    kernel_printf("========================================\n");
    kernel_printf("Initializing kernel...\n\n");

    // Initialize memory management
    kernel_printf("[INIT] Memory Manager...");
    mm_init();
    kernel_state.total_memory = mm_get_total();
    kernel_state.free_memory = mm_get_free();
    kernel_printf(" OK (%d MB total)\n", kernel_state.total_memory / (1024*1024));

    // Initialize process scheduler
    kernel_printf("[INIT] Process Scheduler...");
    proc_init();
    kernel_printf(" OK\n");

    // Initialize filesystem
    kernel_printf("[INIT] Filesystem (NeilerFS)...");
    fs_init();
    kernel_printf(" OK\n");

    // Initialize device drivers
    kernel_printf("[INIT] Device Drivers...");
    dev_init();
    kernel_printf(" OK\n");

    // Initialize network stack
    kernel_printf("[INIT] Network Stack...");
    net_init();
    kernel_printf(" OK\n");

    // Set hostname
    strcpy(kernel_state.hostname, "neiler-64");

    kernel_state.initialized = true;
    kernel_printf("\n[OK] Kernel initialization complete!\n");
    kernel_printf("Hostname: %s\n", kernel_state.hostname);
    kernel_printf("Ready for developer workloads.\n\n");
}

/**
 * Kernel main loop
 */
void kernel_main(void) {
    kernel_init();

    // Start init process (PID 1)
    proc_create("/sbin/init", NULL, PROC_PRIORITY_HIGH);

    // Enable interrupts
    enable_interrupts();

    // Main kernel loop
    while (1) {
        // Schedule next process
        proc_schedule();

        // Update uptime
        kernel_state.uptime++;

        // Handle pending interrupts
        interrupt_handle_pending();

        // Idle if no processes ready
        if (proc_get_ready_count() == 0) {
            cpu_idle();
        }
    }
}

/**
 * System call handler
 */
int64_t syscall_handler(uint32_t syscall_num, uint64_t arg1, uint64_t arg2,
                        uint64_t arg3, uint64_t arg4) {
    switch (syscall_num) {
        case SYS_READ:
            return sys_read((int)arg1, (void*)arg2, (size_t)arg3);

        case SYS_WRITE:
            return sys_write((int)arg1, (const void*)arg2, (size_t)arg3);

        case SYS_OPEN:
            return sys_open((const char*)arg1, (int)arg2, (mode_t)arg3);

        case SYS_CLOSE:
            return sys_close((int)arg1);

        case SYS_FORK:
            return sys_fork();

        case SYS_EXEC:
            return sys_exec((const char*)arg1, (char**)arg2, (char**)arg3);

        case SYS_EXIT:
            sys_exit((int)arg1);
            return 0; // Never reached

        case SYS_MMAP:
            return (int64_t)sys_mmap((void*)arg1, (size_t)arg2, (int)arg3, (int)arg4);

        case SYS_MUNMAP:
            return sys_munmap((void*)arg1, (size_t)arg2);

        case SYS_GETPID:
            return sys_getpid();

        case SYS_KILL:
            return sys_kill((pid_t)arg1, (int)arg2);

        case SYS_SOCKET:
            return sys_socket((int)arg1, (int)arg2, (int)arg3);

        case SYS_BIND:
            return sys_bind((int)arg1, (const struct sockaddr*)arg2, (socklen_t)arg3);

        case SYS_CONNECT:
            return sys_connect((int)arg1, (const struct sockaddr*)arg2, (socklen_t)arg3);

        default:
            return -ENOSYS; // Unknown syscall
    }
}

/**
 * Kernel panic handler
 */
void kernel_panic(const char* message) {
    disable_interrupts();

    kernel_printf("\n\n");
    kernel_printf("*******************************************\n");
    kernel_printf("*         KERNEL PANIC                   *\n");
    kernel_printf("*******************************************\n");
    kernel_printf("\n%s\n\n", message);
    kernel_printf("System halted.\n");

    // Halt CPU
    while (1) {
        cpu_halt();
    }
}

/**
 * Get kernel version string
 */
const char* kernel_get_version(void) {
    static char version[128];
    snprintf(version, sizeof(version), "Neiler-OS %d.%d.%d (%s)",
        NEILER_OS_VERSION_MAJOR,
        NEILER_OS_VERSION_MINOR,
        NEILER_OS_VERSION_PATCH,
        NEILER_OS_CODENAME);
    return version;
}

/**
 * Get system information
 */
void kernel_get_sysinfo(struct sysinfo* info) {
    info->uptime = kernel_state.uptime;
    info->totalram = kernel_state.total_memory;
    info->freeram = mm_get_free();
    info->procs = proc_get_count();
}
