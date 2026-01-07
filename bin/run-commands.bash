# bash completion:
# https://www.gnu.org/software/bash/manual/bash.html#Programmable-Completion

_completion_loader_one()
{
    tog complete $3 $2
}
complete -df -F _completion_loader_one tog