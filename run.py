from etipster import *

if __name__ == "__main__":
    todayMatches = getTodayMatches()
    print(f"{len(todayMatches)} PARTITE OGGI")

    filteredMatches = filterMatches(todayMatches)
    print(f"{len(filteredMatches)} PARTITE FILTRATE E POTENZIALI")

    ticket = createTicket(filteredMatches)
    
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++\n")

    for match, odds in ticket.items():
        print(f"{match} || {odds}\n")

    print("+++++++++++++++++++++++++++++++++++++++++")
    print("+++++++++++++++++++++++++++++++++++++++++\n")