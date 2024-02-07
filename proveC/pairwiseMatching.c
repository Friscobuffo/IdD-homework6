#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "cJSON.h"

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

#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))

#define INSERTION_COST 0.4
#define DELETION_COST 0.4
#define SUBSTITUTION_COST 2

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
        cJSON* attribute = cJSON_GetObjectItemCaseSensitive(first, attribute_name);
        if (attribute->valuestring == "") {
            attribute->valuestring = cJSON_GetObjectItemCaseSensitive(second, attribute_name)->valuestring;
        }
        current = current->next;
    }
}

int main() {
    // reading json file
    FILE* file;
    char* json_string;
    long file_size;
    file = fopen("jsonFile.json", "rb");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    rewind(file);
    json_string = (char*)malloc(file_size * sizeof(char));
    if (json_string == NULL) {
        perror("Memory allocation error");
        return 1;
    }
    fread(json_string, sizeof(char), file_size, file);
    fclose(file);

    // parsing json file
    cJSON* json_array = cJSON_Parse(json_string);
    if (json_array == NULL) {
        printf("Error parsing JSON: %s\n", cJSON_GetErrorPtr());
        return 1;
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
    json_item_outer = json_array->child;
    while (json_item_outer) {
        cJSON* name_outer = cJSON_GetObjectItemCaseSensitive(json_item_outer, "company_name");
        char* company_name_outer = name_outer->valuestring;
        char* company_name_outer_cleaned = removeNonAlphanumeric(company_name_outer);
        int j = i+1;
        json_item_inner = json_item_outer->next;
        while (json_item_inner) {
            comparisonsDone++;
            if (!removed[j]) {
                cJSON* name_inner = cJSON_GetObjectItemCaseSensitive(json_item_inner, "company_name");
                char* company_name_inner = name_inner->valuestring;
                char* company_name_inner_cleaned = removeNonAlphanumeric(company_name_inner);
                float distance = levenshteinDistance(company_name_outer_cleaned, company_name_inner_cleaned);
                if (distance < 0.13) {
                    removed[j] = 1;
                    mergeSecondJsonIntoFirst(json_item_inner, json_item_outer);
                    matchesFound++;
                }
                free(company_name_inner_cleaned);
            }
            j++;
            json_item_inner = json_item_inner->next;
        }
        printf("\rcurrent elem: %d, comparisons done: %d, matches found: %d", i, comparisonsDone, matchesFound);
        fflush(stdout);
        i++;
        json_item_outer = json_item_outer->next;
        free(company_name_outer_cleaned);
    }
    printf("\n");

    // creating copy without duplicates
    cJSON* output_array = cJSON_CreateArray();
    if (output_array == NULL) {
        printf("Error creating cJSON array.\n");
        return 1;
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
        return 1;
    }
    file = fopen("output.json", "w");
    if (file == NULL) {
        printf("Error opening file for writing.\n");
        return 1;
    }
    fputs(json_string, file);
    fclose(file);
    free(json_string);

    // freeing heap
    cJSON_Delete(json_array);
    cJSON_Delete(output_array);
    return 0;
}