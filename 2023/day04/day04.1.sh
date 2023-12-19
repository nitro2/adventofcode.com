awk -F ':' ' {print $2}' | awk -F '|' 'BEGIN{
    sum=0
}
{
    m=split($1, winnum, " ")
    n=split($2, mynum, " ")
    # printf("%s-\n",$2)
    count=0

    printf("Win num: ")
    for (i = 1; i <= m; i++) printf("%d-", winnum[i])
    printf("\nMy num: ")
    for (i = 1; i <= n; i++) printf("%d-", mynum[i])
    printf("\n")

    for (i = 1; i <= n; i++) {
        if ( mynum[i] in winnum ) {
            count += 1
        }
    };

    if (count > 0) {
        printf("count=%d\n", count)
        sum += 2**(count-1)
    }

    printf("\n")
}
END {
    print sum
}
'