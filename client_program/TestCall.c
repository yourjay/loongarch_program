#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == -1) {
        fprintf(stderr, "Failed to create child process\n");
        return 1;
    } else if (pid == 0) {
        // 子进程中执行Python文件
        execlp("python3","python3","/home/root/chenzihan/camera3.py",NULL);
        fprintf(stderr, "Failed to execute Python file\n");
        return 1;
    } else {
        // 父进程中等待子进程结束
        wait(NULL);
        printf("Child process finished\n");
    }

    return 0;
}

