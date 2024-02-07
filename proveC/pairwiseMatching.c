#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "cJSON.h"

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

int main() {
    char* s1 = "samsung";
    char* s2 = "samsung s.p.a";

    char* s1_cleaned = removeNonAlphanumeric(s1);
    char* s2_cleaned = removeNonAlphanumeric(s2);

    float distance = levenshteinDistance(s1_cleaned, s2_cleaned);
    printf("'%s' - '%s'\n", s1_cleaned, s2_cleaned);
    printf("Levenshtein distance between '%s' and '%s' is %f\n", s1, s2, distance);




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

    cJSON *json_array = cJSON_Parse(json_string);
    if (json_array == NULL) {
        printf("Error parsing JSON: %s\n", cJSON_GetErrorPtr());
        return 1;
    }
    free(json_string);

    cJSON* json_item_outer = NULL;
    cJSON* json_item_inner = NULL;
    int i = 0;
    cJSON_ArrayForEach(json_item_outer, json_array) {
        cJSON* name_outer = cJSON_GetObjectItemCaseSensitive(json_item_outer, "company_name");
        char* company_name_outer = name_outer->valuestring;
        char* company_name_outer_cleaned = removeNonAlphanumeric(company_name_outer);
        cJSON_ArrayForEach(json_item_inner, json_array) {
            i++;
            printf("\r%d", i);
            fflush(stdout);
            cJSON *name_inner = cJSON_GetObjectItemCaseSensitive(json_item_inner, "company_name");
            char* company_name_inner = name_inner->valuestring;
            char* company_name_inner_cleaned = removeNonAlphanumeric(company_name_inner);
            float distance = levenshteinDistance(company_name_outer_cleaned, company_name_inner_cleaned);
            // if (distance < 0.15)
            //     printf("Levenshtein distance between '%s' and '%s' is %f\n", company_name_outer, company_name_inner, distance);
            free(company_name_inner_cleaned);
        }
        free(company_name_outer_cleaned);
    }
    cJSON_Delete(json_array);
    return 0;
}
