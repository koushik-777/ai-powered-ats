class Shortlister:
    def __init__(self):
        self.default_threshold = 70.0  # Default match threshold (%)
        self.diversity_boost = 5.0  # Diversity consideration boost (%)
    
    def shortlist(self, candidates, threshold=None, max_candidates=10, diversity_enabled=True):
        """
        Filter and rank candidates based on match scores
        
        Args:
            candidates (list): List of candidates with match scores
            threshold (float, optional): Minimum match score threshold
            max_candidates (int, optional): Maximum number of candidates to shortlist
            diversity_enabled (bool): Whether to apply diversity considerations
            
        Returns:
            list: Shortlisted candidates with justifications
        """
        if threshold is None:
            threshold = self.default_threshold
        
        # Filter candidates by threshold
        qualified_candidates = [c for c in candidates if c["match_score"]["overall_score"] >= threshold]
        
        if diversity_enabled:
            qualified_candidates = self._apply_diversity_considerations(qualified_candidates)
        
        # Sort by match score (descending)
        shortlisted = sorted(
            qualified_candidates, 
            key=lambda x: x["match_score"]["overall_score"], 
            reverse=True
        )
        
        # Add justification for each shortlisted candidate
        for candidate in shortlisted:
            candidate["justification"] = self._generate_justification(candidate)
        
        return shortlisted[:max_candidates]
    
    def _apply_diversity_considerations(self, candidates):
        """Apply diversity considerations to the candidate ranking"""
        # Placeholder for diversity logic
        # In a real implementation, this would analyze the candidate pool
        # and potentially adjust scores to promote diversity
        return candidates
    
    def _generate_justification(self, candidate):
        """Generate justification for shortlisting a candidate"""
        # Placeholder implementation
        justification = f"Candidate matched {candidate['match_score']['overall_score']:.1f}% of job requirements"
        
        # Add specific strength highlights based on match breakdown
        strengths = []
        if "breakdown" in candidate["match_score"]:
            breakdown = candidate["match_score"]["breakdown"]
            
            # Example logic to identify strengths
            if breakdown.get("skills", {}).get("matched"):
                skills_count = len(breakdown["skills"]["matched"])
                strengths.append(f"Matched {skills_count} key skills")
        
        if strengths:
            justification += ". Key strengths: " + ", ".join(strengths)
        
        return justification