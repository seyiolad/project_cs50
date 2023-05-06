// #include <stdio.h>

// int main(void)
// {
//     for (int i = 0; i <= 3; i++)
//     {
//         printf("#\n");
//     }
// }


#include <stdio.h>
#include <stdlib.h>

#define MAX_CANDIDATES 10
#define MAX_VOTERS 100

int main()
{
    int num_candidates, num_voters;
    int votes[MAX_VOTERS][MAX_CANDIDATES]; // 2D array to store the ranked choices of each voter
    int eliminated[MAX_CANDIDATES] = {0}; // array to keep track of eliminated candidates
    int num_votes[MAX_CANDIDATES] = {0}; // array to keep track of the number of votes each candidate receives
    int i, j, k, max_votes, min_votes, min_candidate, winner;

    // get input from user
    printf("Enter the number of candidates: ");
    scanf("%d", &num_candidates);
    printf("Enter the number of voters: ");
    scanf("%d", &num_voters);

    // get the ranked choices of each voter
    for (i = 0; i < num_voters; i++) {
        printf("Enter the ranked choices of voter %d: ", i + 1);
        for (j = 0; j < num_candidates; j++) {
            scanf("%d", &votes[i][j]);
        }
    }

    // conduct the run-off election
    while (1) {
        // reset the number of votes for each candidate
        for (i = 0; i < num_candidates; i++) {
            num_votes[i] = 0;
        }

        // count the number of first-choice votes for each candidate
        for (i = 0; i < num_voters; i++) {
            for (j = 0; j < num_candidates; j++) {
                if (!eliminated[votes[i][j]]) {
                    num_votes[votes[i][j]]++;
                    break;
                }
            }
        }

        // find the candidate with the most votes
        max_votes = -1;
        winner = -1;
        for (i = 0; i < num_candidates; i++) {
            if (!eliminated[i] && num_votes[i] > max_votes) {
                max_votes = num_votes[i];
                winner = i;
            }
        }

        // check if a candidate has a majority of votes
        if (max_votes > num_voters / 2) {
            printf("Candidate %d wins with %d votes!\n", winner + 1, max_votes);
            break;
        }

        // check if there is a tie for the most votes
        for (i = 0; i < num_candidates; i++) {
            if (i != winner && !eliminated[i] && num_votes[i] == max_votes) {
                printf("There is a tie between candidates %d and %d!\n", winner + 1, i + 1);
                break;
            }
        }
        if (i != num_candidates) {
            break;
        }

        // eliminate the candidate with the least number of votes
        min_votes = num_voters + 1;
        for (i = 0; i < num_candidates; i++) {
            if (!eliminated[i] && num_votes[i] < min_votes) {
                min_votes = num_votes[i];
                min_candidate = i;
            }
        }
        eliminated[min_candidate] = 1;
        printf("Candidate %d has been eliminated.\n", min_candidate + 1);
    }

    return 0;
}
