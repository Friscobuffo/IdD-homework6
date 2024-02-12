#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "cJSON.h"
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>

// to compile run:
// gcc -o prova pairwiseMatching.c cJSON.c

char* removeNonAlphanumeric(char *str) {
    size_t len = strlen(str);
    char* result = (char*)malloc((len+1)*sizeof(char));
    char* src = (char*)str;
    char* dst = result;
    while (*src) {
        if (isalnum((unsigned char)*src))
            *dst++ = *src;
        src++;
    }
    *dst = '\0';
    return result;
}

void toLowercase(char *str) {
    while (*str) {
        *str = tolower(*str);
        str++;
    }
}

#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))

#define INSERTION_COST 1
#define DELETION_COST 1
#define SUBSTITUTION_COST 2.5

float levenshteinDistance(char *s1, char *s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);
    float dp[len1 + 1][len2 + 1];
    for (int i = 0; i <= len1; i++)
        dp[i][0] = i * DELETION_COST;
    for (int j = 0; j <= len2; j++)
        dp[0][j] = j * INSERTION_COST;
    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            if (s1[i - 1] == s2[j - 1])
                dp[i][j] = dp[i - 1][j - 1];
            else
                dp[i][j] = MIN3(dp[i - 1][j] + DELETION_COST, dp[i][j - 1] + INSERTION_COST, dp[i - 1][j - 1] + SUBSTITUTION_COST);
        }
    }
    int max_distance = len1 > len2 ? len1 : len2;
    return (float)dp[len1][len2] / max_distance;
}

void mergeSecondJsonIntoFirst(cJSON* first, cJSON* second) {
    cJSON* current = first->child;
    while (current != NULL) {
        char* attribute_name = current->string;
        current = current->next;
        cJSON* attribute = cJSON_GetObjectItemCaseSensitive(first, attribute_name);
        if (attribute->valuestring == NULL) {
            attribute->valuestring = (char*)malloc(sizeof(char));
            attribute->valuestring[0] = '\0';
        }
        if (strcmp(attribute->valuestring, "") == 0) {
            char* value = cJSON_GetObjectItemCaseSensitive(second, attribute_name)->valuestring;
            if (value == NULL) continue;
            char* copy = (char*)malloc((strlen(value)+1) * sizeof(char));
            strcpy(copy, value);
            free(attribute->valuestring);
            attribute->valuestring = copy;
        }
    }
}

void computePairwiseMatchingOnJson(char* jsonFilePath, char* outputFilePath, int* totalElementsRemoved) {
    printf("computing: %s\n", jsonFilePath);
    // reading json file
    FILE* file;
    char* json_string;
    long file_size;
    file = fopen(jsonFilePath, "rb");
    if (file == NULL) {
        perror("Error opening file");
        exit(1);
    }
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    rewind(file);
    json_string = (char*)malloc(file_size * sizeof(char));
    if (json_string == NULL) {
        perror("Memory allocation error");
        exit(1);
    }
    fread(json_string, sizeof(char), file_size, file);
    fclose(file);

    // parsing json file
    cJSON* json_array = cJSON_Parse(json_string);
    if (json_array == NULL) {
        printf("Error parsing JSON: %s\n", cJSON_GetErrorPtr());
        exit(1);
    }
    free(json_string);

    // finding duplicates
    cJSON* json_item_outer = NULL;
    cJSON* json_item_inner = NULL;
    
    int numberOfEntries = cJSON_GetArraySize(json_array);
    int removed[numberOfEntries];
    for (int i=0; i<numberOfEntries; i++)
        removed[i] = 0;
    int i = 0;
    int comparisonsDone = 0;
    int matchesFound = 0;
    for (json_item_outer = json_array->child; json_item_outer != NULL; json_item_outer = json_item_outer->next, i++) {
        if (removed[i])
            continue;
        cJSON* name_outer = cJSON_GetObjectItemCaseSensitive(json_item_outer, "company_name");
        char* company_name_outer = name_outer->valuestring;
        char* company_name_outer_cleaned = removeNonAlphanumeric(company_name_outer);
        toLowercase(company_name_outer_cleaned);
        int j = i+1;
        for (json_item_inner = json_item_outer->next; json_item_inner != NULL; json_item_inner = json_item_inner->next, j++) {
            if (removed[j])
                continue;
            comparisonsDone++;
            cJSON* name_inner = cJSON_GetObjectItemCaseSensitive(json_item_inner, "company_name");
            char* company_name_inner = name_inner->valuestring;
            char* company_name_inner_cleaned = removeNonAlphanumeric(company_name_inner);
            toLowercase(company_name_inner_cleaned);
            float distance = levenshteinDistance(company_name_outer_cleaned, company_name_inner_cleaned);
            if (distance < 0.3) {
                removed[j] = 1;
                mergeSecondJsonIntoFirst(json_item_outer, json_item_inner);
                matchesFound++;
                // if (((double)rand() / RAND_MAX) < 0.01) {
                //     printf("\nmatch, %s --- %s\n", company_name_inner, company_name_outer);
                //     fflush(stdout);
                // }
            }
            free(company_name_inner_cleaned);
        }
        printf("\rcurrent elem: %d, comparisons done: %d, matches found: %d", i, comparisonsDone, matchesFound);
        fflush(stdout);
        free(company_name_outer_cleaned);
    }
    printf("\n");

    // creating copy without duplicates
    *totalElementsRemoved = *totalElementsRemoved + matchesFound;
    cJSON* output_array = cJSON_CreateArray();
    if (output_array == NULL) {
        printf("Error creating cJSON array.\n");
        exit(1);
    }
    i = 0;
    cJSON_ArrayForEach(json_item_outer, json_array) {
        if (!removed[i]) {
            cJSON* copy = cJSON_CreateObject();
            cJSON* child = json_item_outer->child;
            while (child) {
                char* attribute_name = child->string;
                char* attribute_value = cJSON_GetObjectItemCaseSensitive(json_item_outer, attribute_name)->valuestring;
                cJSON* jsonString = cJSON_CreateString(attribute_value);
                cJSON_AddItemToObject(copy, attribute_name, jsonString);
                child = child->next;
            }
            cJSON_AddItemToArray(output_array, copy);
        }
        i++;
    }

    // saving to file
    json_string = cJSON_Print(output_array);
    if (json_string == NULL) {
        printf("Error converting cJSON object to JSON string.\n");
        exit(1);
    }
    file = fopen(outputFilePath, "w");
    if (file == NULL) {
        printf("Error opening file for writing.\n");
        exit(1);
    }
    fputs(json_string, file);
    fclose(file);
    free(json_string);

    // freeing heap
    cJSON_Delete(json_array);
    cJSON_Delete(output_array);
}

#define BLOCKS_DIRECTORY "custom-blocks"
#define OUTPUT_DIRECTORY "output"

int main() {
    srand(time(NULL));
    char command[100];
    sprintf(command, "rm -r %s", OUTPUT_DIRECTORY);
    if (system(command) != 0) {
        perror("Error removing directory");
        return 1;
    }
    mkdir(OUTPUT_DIRECTORY, 0777);

    DIR *directory;
    struct dirent *entry;
    directory = opendir(BLOCKS_DIRECTORY);
    if (directory == NULL) {
        perror("Unable to open directory");
        return 1;
    }
    char path[200];
    char outputPath[200];
    int totalElementsRemoved = 0;
    while ((entry = readdir(directory)) != NULL) {
        char* jsonName = entry->d_name;
        if (strcmp(jsonName,  ".json") == 0)
            continue;
        if (strlen(jsonName) > 2) {
            path[0] = '\0';
            strcat(path, BLOCKS_DIRECTORY);
            strcat(path, "/");
            strcat(path, jsonName);

            outputPath[0] = '\0';
            strcat(outputPath, OUTPUT_DIRECTORY);
            strcat(outputPath, "/");
            strcat(outputPath, jsonName);
            computePairwiseMatchingOnJson(path, outputPath, &totalElementsRemoved);
        }
    }
    printf("total elements removed: %d\n", totalElementsRemoved);
    closedir(directory);
    return 0;
}