"""
TraitBlender Transform Pipeline

A factory pipeline for creating and managing multiple transforms.
"""

from .transforms import Transform


class TransformPipeline:
    """
    A pipeline that manages multiple transforms and executes them in sequence.
    
    The pipeline acts as a factory for creating transforms and provides
    methods to run all transforms in order and undo them in reverse order.
    
    Example:
        pipeline = TransformPipeline()
        pipeline.add_transform("world.color", "dirichlet", {"alphas": [0.3, 0.3, 0.3, 1]})
        pipeline.add_transform("camera.location", "normal", {"mu": 0, "sigma": 1, "n": 3})
        pipeline.run()  # Execute all transforms
        pipeline.undo()  # Undo all transforms in reverse order
    """
    
    def __init__(self, name: str = "TransformPipeline"):
        """
        Initialize a new transform pipeline.
        
        Args:
            name (str): Name for the pipeline (for identification)
        """
        self.name = name
        self._transforms = []  # List of Transform objects
        self._execution_history = []  # Track execution state
    
    def add_transform(self, property_path: str, sampler_name: str, params: dict = None) -> 'TransformPipeline':
        """
        Add a new transform to the pipeline and initialize it.
        
        Args:
            property_path (str): Relative property path (e.g., 'world.color')
            sampler_name (str): Name of the sampler function
            params (dict): Parameters for the sampler
            
        Returns:
            TransformPipeline: Self for method chaining
            
        Example:
            pipeline.add_transform("world.color", "uniform", {"low": 0, "high": 1})
        """
        transform = Transform(property_path, sampler_name, params)
        self._transforms.append(transform)
        print(f"Added transform #{len(self._transforms)}: {transform}")
        return self
    
    def __call__(self) -> list:
        """
        Execute all transforms in the pipeline in the order they were added.
        
        Returns:
            list: List of results from each transform execution
            
        Example:
            results = pipeline()
        """
        if not self._transforms:
            print(f"Pipeline '{self.name}' is empty - no transforms to run")
            return []
        
        print(f"\n=== Running Pipeline: {self.name} ===")
        print(f"Executing {len(self._transforms)} transforms...")
        
        results = []
        for i, transform in enumerate(self._transforms, 1):
            print(f"\n--- Transform {i}/{len(self._transforms)} ---")
            try:
                result = transform()
                results.append(result)
                print(f"✓ Transform {i} completed successfully")
            except Exception as e:
                print(f"✗ Transform {i} failed: {e}")
                # Continue with remaining transforms
                results.append(None)
        
        self._execution_history.append("run")
        print(f"\n=== Pipeline '{self.name}' completed ===")
        return results

    def run(self) -> list:
        """
        Execute all transforms in the pipeline in the order they were added.
        
        Returns:
            list: List of results from each transform execution
            
        Example:
            results = pipeline.run()
        """
        return self()
    
    def undo(self) -> list:
        """
        Undo all transforms in the pipeline in reverse order.
        
        Returns:
            list: List of undo results from each transform
            
        Example:
            undo_results = pipeline.undo()
        """
        if not self._transforms:
            print(f"Pipeline '{self.name}' is empty - no transforms to undo")
            return []
        
        print(f"\n=== Undoing Pipeline: {self.name} ===")
        print(f"Undoing {len(self._transforms)} transforms in reverse order...")
        
        undo_results = []
        # Undo in reverse order (last applied first)
        for i in range(len(self._transforms) - 1, -1, -1):
            transform = self._transforms[i]
            transform_index = i + 1
            print(f"\n--- Undoing Transform {transform_index}/{len(self._transforms)} ---")
            try:
                transform.undo_all()
                undo_results.append(True)
                print(f"✓ Transform {transform_index} undone successfully")
            except Exception as e:
                print(f"✗ Transform {transform_index} undo failed: {e}")
                undo_results.append(False)
        
        self._execution_history.append("undo")
        print(f"\n=== Pipeline '{self.name}' undo completed ===")
        return undo_results
    
    def clear(self):
        """Clear all transforms from the pipeline."""
        count = len(self._transforms)
        self._transforms.clear()
        self._execution_history.clear()
        print(f"Cleared {count} transforms from pipeline '{self.name}'")
    
    def get_transform_count(self) -> int:
        """Get the number of transforms in the pipeline."""
        return len(self._transforms)
    
    def get_execution_history(self) -> list:
        """Get the execution history of the pipeline."""
        return self._execution_history.copy()
    
    def __str__(self):
        """Return a summary of the pipeline."""
        lines = []
        lines.append(f"=== Transform Pipeline: {self.name} ===")
        lines.append(f"Transforms: {len(self._transforms)}")
        lines.append(f"Execution History: {self._execution_history}")
        
        if self._transforms:
            lines.append("\nTransforms:")
            for i, transform in enumerate(self._transforms, 1):
                lines.append(f"  {i}. {transform}")
        
        return "\n".join(lines)
    
    def summarize(self):
        """Print a summary of the pipeline."""
        print(self.__str__())
    
    def print_detailed(self):
        """Print detailed information about each transform."""
        lines = []
        lines.append(f"=== Detailed Pipeline Info: {self.name} ===")
        lines.append(f"Total transforms: {len(self._transforms)}")
        lines.append(f"Execution history: {self._execution_history}")
        
        if not self._transforms:
            lines.append("No transforms in pipeline")
            return "\n".join(lines)
        
        for i, transform in enumerate(self._transforms, 1):
            lines.append(f"\n--- Transform {i} ---")
            lines.append(f"Property: {transform.property_path}")
            lines.append(f"Sampler: {transform.sampler_name}")
            lines.append(f"Parameters: {transform.params}")
            
            # Show transform history if available
            history = transform.get_history()
            if history:
                lines.append(f"History: {len(history)} values cached")
                if len(history) <= 3:
                    lines.append(f"  Values: {history}")
                else:
                    lines.append(f"  Values: {history[:2]} ... {history[-1]}")
        
        return "\n".join(lines)
    
    def __repr__(self):
        return f"TransformPipeline(name='{self.name}', transforms={len(self._transforms)})"
    
    def __getitem__(self, index):
        """
        Get a transform by index.
        
        Args:
            index (int): Index of the transform (0-based)
            
        Returns:
            Transform: The transform at the specified index
            
        Raises:
            IndexError: If index is out of range
        """
        return self._transforms[index]
    
    def __len__(self):
        return len(self._transforms)
    
    def __bool__(self):
        return len(self._transforms) > 0

    def to_dict(self):
        """Serialize the pipeline to a list of transform dicts."""
        return [t.to_dict() for t in self._transforms]

    @classmethod
    def from_dict(cls, d, name="TransformPipeline"):
        """Create a TransformPipeline from a list of transform dicts."""
        pipeline = cls(name=name)
        for t_dict in d:
            pipeline._transforms.append(Transform.from_dict(t_dict))
        return pipeline

    def __iter__(self):
        """Iterate over transforms in the pipeline."""
        return iter(self._transforms)

    def __setitem__(self, index, value):
        """Set a transform at a specific index."""
        self._transforms[index] = value


def register():
    pass


def unregister():
    pass 