class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state
        self.chickens = start_state[0] # No: of chickens on shore
        self.foxes = start_state[1] # No: of foxes on shore

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list
        successors = []
        chickens = state[0]
        foxes = state[1]
        boat = state[2] # 1 for current shore, 0 for opposite shore
        if boat == 1: 
            move_b = 0 # this swaps boat condition from 1 to 0
        else:
            move_b = 1 # similar swap from 0 to 1
        
        moves = [(2, 0), (1, 0), (1, 1), (0, 1), (0, 2)] # all possible moves without fox eating chicken
        for move in moves:
            move_c = move[0] # chicken
            move_f = move[1] # fox

            if boat == 1: # boat is on current shore
                res = ((chickens - move_c), (foxes - move_f), move_b) # subtract c & f to be moved, update boat condition
            else: # boat is on opp shore
                res = ((chickens + move_c), (foxes + move_f), move_b) # add c & f to be moved, update boat condition
            if (0 <= res[0] and res[0] <= self.chickens and 0 <= res[1] and res[1] <= self.foxes): # valid condition check
                # safety on current shore / safety on opp shore
                # no: of chickens either >= no: of foxes, or no: of chickens == 0
                if (res[0] >= res[1] or res[0] == 0) and (self.chickens-res[0] >= self.foxes-res[1] or self.chickens-res[0] == 0):
                    successors.append(res)
        
        return successors 

    # I also had a goal test method. You should write one.
    def goal_test(self, state):
        return state == self.goal_state # returns true if state matches our goal state


    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
