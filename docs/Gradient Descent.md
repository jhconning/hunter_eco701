

## Lesson Summary: Optimization in Theory vs. Computation

### 1. The Core Equivalence

Whether minimizing input costs for a firm or minimizing prediction error in OLS, the computational algorithm is identical: **Gradient Descent**.

  

$$\mathbf{\theta}^{(t+1)} = \mathbf{\theta}^{(t)} - \alpha \nabla J(\mathbf{\theta}^{(t)})$$

|**Domain**|**Choice Variables (θ)**|**Objective Function (J)**|**Stopping Condition (∇J=0)**|
|---|---|---|---|
|**Microeconomics**|Inputs $(K, L)$|Expenditure / Penalty|Tangency ($MRTS = \frac{w}{r}$)|
|**Econometrics (OLS)**|Parameters $(\beta_0, \beta_1)$|Sum of Squared Residuals|Orthogonality ($\sum e_i x_i = 0$)|

### 2. Analytical vs. Computational Constraints

- **Whiteboard (Lagrangian Method):**
    
      
    
    $$\mathcal{L}(K, L, \lambda) = rK + wL + \lambda [Q_0 - f(K, L)]$$
    
    - _Mechanism:_ Symbolic solution to $\nabla \mathcal{L} = \mathbf{0}$.
        
          
        
    - _Economics:_ $\lambda$ acts as a constant **shadow price** ($\lambda = MC$).
        
          
        
    - _Computational Flaw:_ Creates a **saddle-point problem**. Standard gradient descent on $\mathcal{L}$ directly oscillates or explodes.
        
          
        
- **Computer Solver (Penalty / Loss Method):**
    
      
    
    $$J(K, L) = rK + wL + \frac{\gamma}{2} [Q_0 - f(K, L)]^2$$
    
    - _Mechanism:_ Converts constrained optimization into an unconstrained smooth surface.
        
          
        
    - _Economics:_ The effective shadow price $\lambda_{\text{eff}} = \gamma (Q_0 - Q)$ acts as a dynamic restoring force proportional to the output gap.
        
          
        
    - _Computational Advantage:_ Converts saddle points into stable local minima that gradient descent can solve iteratively.
        
          
        

### Key Takeaway for Students

> Symbolic micro theory uses linear constraints ($\lambda$) to extract neat economic interpretations like marginal cost. Numerical solvers (SciPy, machine learning packages) rewrite those constraints as **squared penalties** behind the scenes so that gradient descent algorithms can converge stably.