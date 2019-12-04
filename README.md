# evoman-artificial-intelligence

Code, docs for an AI based agent to play evoman game.

**NOTE:**  Inside evoman folder is the game content, you can read more about its implementation and the excellent work done by **karinemiras** [here](https://github.com/karinemiras/evoman_framework).  *We only created agents to play the game, all evoman code is not ours.*

## Requirements

    pip install -r requirements.txt
    


## Code Structure

To evolve an agent using neuroevolution you can run:

    python agents/neuroevolution.py

Inside the same file you can configure a few parameters:

    population_size
    number_of_generations
    mutate_rate

You can give your experiment a name on and the best models after evolution will be saved on

    models/

## Best Model
To run the best model choosed for the final project, you can simply do:

    python run_example.py

By default, I included the best solution so far.







