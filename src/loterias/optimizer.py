import random
import numpy as np
from typing import List, Dict, Tuple
from .backtester import Backtester
from .base import Lottery

class GeneticOptimizer:
    def __init__(self, lottery: Lottery, game_config: Dict, population_size: int = 20, generations: int = 10, mutation_rate: float = 0.1):
        self.lottery = lottery
        self.game_config = game_config
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
        # Ranges for weights: 0.0 to 10.0
        self.gene_min = 0.0
        self.gene_max = 10.0
        
        # Determine prize tiers for fitness
        self.prize_tiers = self._get_prize_tiers(lottery.slug)

    def _get_prize_tiers(self, slug: str) -> List[int]:
        if slug == 'megasena': return [4, 5, 6]
        if slug == 'quina': return [2, 3, 4, 5]
        if slug == 'lotofacil': return [11, 12, 13, 14, 15]
        return [] # Default: no specific tiers, just max

    def _create_individual(self) -> List[float]:
        # Gene: [w_gap, w_freq, w_surf]
        return [random.uniform(self.gene_min, self.gene_max) for _ in range(3)]

    def _calculate_fitness(self, individual: List[float]) -> float:
        w_gap, w_freq, w_surf = individual
        
        # Setup Backtester
        # We test on fewer draws for speed during evolution, e.g., last 50
        # User said "don't pity the computer", so let's do 50 decent draws.
        draws_to_test = 50 
        
        backtester = Backtester(
            lottery=self.lottery,
            model_type='hybrid',
            model_args={'w_gap': w_gap, 'w_freq': w_freq, 'w_surf': w_surf},
            range_min=self.game_config['min'],
            range_max=self.game_config['max'],
            draw_count=self.game_config['draw']
        )
        
        # Suppress prints
        try:
            results = backtester.run(draws_to_test=draws_to_test, prediction_size=self.game_config['default_play'], silent=True)
        except Exception as e:
            import sys
            print(f"Error evaluating individual {individual}: {e}", file=sys.stderr)
            return 0.0

        # Calculate Score
        total_score = 0.0
        hits_dist = results.get('hits_distribution', {})
        
        # Base score: sum of all hits (reward getting closer)
        # However, we want to prioritize Prize Tiers.
        
        for hits, count in hits_dist.items():
            # Base value: hit count itself
            score = hits * count 
            
            # Tier Bonus
            if hits in self.prize_tiers:
                # Big bonus for reaching minimum prize
                # e.g. Quadra (4) in MegaSena.
                # If we get 1 quadra, that's worth WAY more than 100 ternos.
                
                # Exponential scaling for higher tiers?
                # Index in prize_tiers: 0 is min prize, -1 is jackpot.
                tier_index = self.prize_tiers.index(hits)
                bonus = 100 * (10 ** tier_index) # 100, 1000, 10000...
                score += bonus * count
            
            total_score += score
            
        return total_score

    def optimize(self):
        print(f"Starting Genetic Optimization for {self.lottery.name}...")
        print(f"Population: {self.population_size}, Generations: {self.generations}")
        
        population = [self._create_individual() for _ in range(self.population_size)]
        
        for gen in range(self.generations):
            # Evaluate Fitness
            fitness_scores = []
            for ind in population:
                fitness_scores.append((ind, self._calculate_fitness(ind)))
            
            # Sort by fitness (descending)
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            best_ind, best_score = fitness_scores[0]
            print(f"Gen {gen+1}: Best Score = {best_score:.2f} | Weights: Gap={best_ind[0]:.2f}, Freq={best_ind[1]:.2f}, Surf={best_ind[2]:.2f}")
            
            # Selection (Elitism + Top 50%)
            top_half = fitness_scores[:self.population_size // 2]
            parents = [ind for ind, score in top_half]
            
            # Next Generation
            new_population = []
            
            # Elitism: Keep best
            new_population.append(best_ind)
            
            while len(new_population) < self.population_size:
                p1 = random.choice(parents)
                p2 = random.choice(parents)
                
                # Crossover (Average)
                child = [(g1 + g2) / 2.0 for g1, g2 in zip(p1, p2)]
                
                # Mutation
                if random.random() < self.mutation_rate:
                    mutate_idx = random.randint(0, 2)
                    child[mutate_idx] += random.uniform(-1.0, 1.0)
                    # Clamp
                    child[mutate_idx] = max(self.gene_min, min(self.gene_max, child[mutate_idx]))
                
                new_population.append(child)
            
            population = new_population
            
        return population[0] # Return best of last gen (elitism ensures it's good)
