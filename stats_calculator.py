# Class that deal with 

class statsCalculator:

        """
            Normalize based on percentile ranges rather than absolute min/max.
            This creates more realistic distributions.
            
            Args:
                value: The stat value to normalize
                percentiles: Dict with keys like 'p10', 'p50', 'p90' representing
                            the 10th, 50th, and 90th percentiles for this stat
        """
        def percentile_normalize(self, value, percentiles):
            if value <= percentiles['p10']:
                return 0.0
            elif value >= percentiles['p90']:
                return 1.0
            elif value <= percentiles['p50']:
                # Linear interpolation between 10th percentile (0.0) and 50th percentile (0.5)
                return 0.5 * (value - percentiles['p10']) / (percentiles['p50'] - percentiles['p10'])
            else:
                # Linear interpolation between 50th percentile (0.5) and 90th percentile (1.0)
                return 0.5 + 0.5 * (value - percentiles['p50']) / (percentiles['p90'] - percentiles['p50'])
        
        def calculate_scoring_ability(self, player_stats):
            # Points per game with realistic ranges
            ppg = player_stats['points'] / player_stats['games']
            ppg_percentiles = {
                'p10': 4.0,   # Bench players
                'p50': 11.5,  # Role players
                'p90': 25.0   # Elite scorers
            }
            
            # True shooting percentage ranges
            ts_percentiles = {
                'p10': 0.48,  # Poor efficiency
                'p50': 0.57,  # League average
                'p90': 0.67   # Elite efficiency
            }
            
            # Usage rate ranges
            usage_percentiles = {
                'p10': 0.12,  # Low usage
                'p50': 0.20,  # Average usage
                'p90': 0.32   # High usage stars
            }
            
            # Calculate component scores
            volume_score = self.percentile_normalize(ppg, ppg_percentiles)
            efficiency_score = self.percentile_normalize(player_stats['ts%'], ts_percentiles)
            usage_score = self.percentile_normalize(player_stats['usage%'], usage_percentiles)
            
            # Weight efficiency most heavily for scoring
            overall_scoring = (
                (efficiency_score * 0.45) +  # Efficiency is king
                (volume_score * 0.35) +      # Volume production matters
                (usage_score * 0.20)         # Context for role
            )
            
            return overall_scoring
        
        def calculate_playmaking(self, player_stats):
            # Assists per game
            apg = player_stats['assists'] / player_stats['games']
            apg_percentiles = {
                'p10': 1.2,   # Non-playmakers
                'p50': 3.1,   # Average
                'p90': 8.5    # Elite playmakers
            }
            
            # Assist-to-turnover ratio
            ast_to = player_stats['assists'] / max(player_stats['turnovers'], 1)
            ast_to_percentiles = {
                'p10': 0.9,   # Poor ball handlers
                'p50': 1.8,   # Average
                'p90': 3.5    # Excellent decision makers
            }
            
            # Turnover percentage (lower is better, so we invert it)
            to_pct_inverted = 1 - player_stats['turnover%']
            to_pct_percentiles = {
                'p10': 1 - 0.18,  # High turnover players
                'p50': 1 - 0.13,  # Average
                'p90': 1 - 0.08   # Great ball security
            }
            
            volume_score = self.percentile_normalize(apg, apg_percentiles)
            ratio_score = self.percentile_normalize(ast_to, ast_to_percentiles)
            security_score = self.percentile_normalize(to_pct_inverted, to_pct_percentiles)
            
            # Balance volume and efficiency
            overall_playmaking = (
                (volume_score * 0.4) +     # Raw assist production
                (ratio_score * 0.4) +      # Decision-making quality
                (security_score * 0.2)     # Ball security
            )
            
            return overall_playmaking
        

        def calculate_rebounding(self, player_stats):
            # Get raw rebounding rate
            rpg = player_stats['rebounds'] / player_stats['games']
            
            # Updated NBA percentiles - raised the elite threshold to better reflect actual distribution
            rpg_percentiles = {
                'p10': 2.2,   # Role players, guards - slightly lower to catch more low rebounders
                'p50': 4.8,   # Average NBA player - lowered to be more realistic
                'p90': 12.8   # Elite rebounders - raised significantly to properly capture Gobert/Sabonis tier
            }
            
            # Updated percentiles for total rebound percentage to better match reality
            trb_percentiles = {
                'p10': 0.05,  # Low-volume players
                'p50': 0.11,  # League average - slightly lower
                'p90': 0.28   # Elite rebounders - raised to capture truly elite rates
            }
            
            # Calculate base scores using percentile normalization
            volume_score = self.percentile_normalize(rpg, rpg_percentiles)
            efficiency_score = self.percentile_normalize(player_stats['rebound%'], trb_percentiles)
            
            # Much more conservative position adjustments to prevent inflation
            position_multipliers = {
                'C': 1.0,     # Centers - baseline expectation
                'PF': 1.01,   # Power forwards - minimal bonus
                'SF': 1.03,   # Small forwards - very small bonus  
                'SG': 1.06,   # Shooting guards - modest bonus
                'PG': 1.10,   # Point guards - reasonable but not excessive bonus
            }
            
            position_factor = position_multipliers.get(player_stats['position'], 1.02)
            
            # Increase volume weighting even more since raw rebounds matter most for team success
            base_score = (volume_score * 0.80) + (efficiency_score * 0.20)
            
            # Apply position adjustment more conservatively
            final_score = min(1.0, base_score * position_factor)
            
            return final_score
        

        def calculate_defensive_ability(self, player_stats):
            # Expanded defensive box plus-minus percentiles to capture elite defenders better
            dbpm_percentiles = {
                'p10': -3.0,  # Poor defenders - expanded range downward
                'p50': 0.0,   # Average - true neutral
                'p90': 4.0    # Elite defenders - expanded upward to capture Gobert-tier impact
            }
            
            # Steal percentage - slightly adjusted based on current league trends
            stl_pct_percentiles = {
                'p10': 0.5,   # Low steal rate
                'p50': 1.3,   # Average - slightly lower
                'p90': 3.0    # High steal rate - raised slightly
            }
            
            # Block percentage - significantly expanded to better capture rim protectors
            blk_pct_percentiles = {
                'p10': 0.3,   # Low block rate
                'p50': 1.0,   # Average - lowered  
                'p90': 6.5    # Elite rim protectors - raised to better capture Gobert's impact
            }
            
            # Position-specific weights for steals vs blocks
            position_weights = {
                'PG': {'steal': 0.8, 'block': 0.2},  # Guards rely heavily on steals
                'SG': {'steal': 0.75, 'block': 0.25}, 
                'SF': {'steal': 0.6, 'block': 0.4},   # Wings more balanced
                'PF': {'steal': 0.35, 'block': 0.65}, # Bigs favor blocks
                'C': {'steal': 0.25, 'block': 0.75}   # Centers heavily weighted toward rim protection
            }
            
            weights = position_weights.get(player_stats['position'], {'steal': 0.5, 'block': 0.5})
            
            # Calculate component scores
            dbpm_score = self.percentile_normalize(player_stats['defensivePlusMinus'], dbpm_percentiles)
            steal_score = self.percentile_normalize(player_stats['steal%'], stl_pct_percentiles)
            block_score = self.percentile_normalize(player_stats['block%'], blk_pct_percentiles)
            
            # Position-weighted steal/block contribution
            steal_block_score = (steal_score * weights['steal']) + (block_score * weights['block'])
            
            # Slightly increased weighting on defensive plus-minus since it's the best overall measure
            overall_defense = (
                (dbpm_score * 0.60) +        # Overall impact most important - increased weight
                (steal_block_score * 0.40)   # Position-specific contributions - decreased weight
            )
            
            return overall_defense



        def fingerprint(self, player_stats):
            fingerprint = {
                'scoring_ability': self.calculate_scoring_ability(player_stats),
                'playmaking': self.calculate_playmaking(player_stats),
                'rebounding': self.calculate_rebounding(player_stats),
                'defense': self.calculate_defensive_ability(player_stats),
                'usage%': player_stats['usage%'],
            }
            return fingerprint