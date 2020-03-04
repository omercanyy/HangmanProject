# HangmanProject
Hangman game is a problem with a great scientific depth. I am taking this game as a real life problem an try to create a solution following similar design and development patterns we can see today's big cooperates (like where I work; Microsoft).

# Goal
Create a bot that plays Hangman game with a great success.

# Plan
Current plan is to create;
1. Hangman Game play API
2. Create 3 bots of different "intelligence"
  a. Random Bot: Just guesses random letters everytime. This a base line for the start of this project
  b. Basic Ingelligent Bot: This bot uses a very basic strategy to fake intelligence where it gives letter by the frequency starting from the most frequent one to the least.
  c. Intelligent Bot: This bot basically will be the product solution we will "ship".

# Methodology
At the very beginning, I need to explore the problem to better understand it. Therefore, I will start very straight forward. But during the design process, I need to think about the possible complexities we might add to out bots, games, and the way we are approaching this problem
## Initial Approach: Explore the problem
My initial approach is to explore the problem with a straight forward baseline and a bot that -I hope- will perform above this baseline. Then create some metrics to better evaluate the performance of our bots. This process goes hand in hand with thinking about different scenarios for this problem to stress-test our bots and see their upper-limits. Or see if is there any scenario where an over intelligent bot either fails or becomes to costly so we might think about a hybrid model.

### Corpus Selection
For corpus selection in the initial approach, I will start with nltk wordnet corpus.

### Metrics
Initial metrics will as simple as a passing rates. And just so we have some flavor to our inital approach I will log how many guesses it took for our bots to pass each game so maybe we can see some interesting scenarios where more intelligent bot might take more guesses to pass a game comparing to a simpler bot.

### Scenarios
With a very shallow analysis of the game complexity. It's obvious that we can have scenarios where the length of the word in play is either too long or too short. Total number of guesses our bots are allowed to make is an other dimension of complexity here. I will have 3 scenarios plus a no-scenario scenario as follows:
  1. No Scenario: Random word picked from the corpus. 10 total guesses.
  2. Short Word (1-6 letters): A word picked from words with length in between 1 and 6 letters (inclusive) 10 total guesses.
  3. Long Word (7-12 letters): A word picked from words with length in between 7 and 12 letters (inclusive) 10 total guesses.
  4. Short word More Guesses (1-6 letters): A word picked from words with length in between 1 and 6 letters (inclusive) 20 total guesses.

