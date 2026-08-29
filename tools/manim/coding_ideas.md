# Integrated Computational Frameworks for Graduate Microeconomic Theory: A Pedagogical Survey for Economics 701

The pedagogical landscape of graduate-level microeconomic theory is undergoing a significant transition, moving from a paradigm defined solely by analytical proofs and Lagrangian derivations toward one that integrates computational modeling, numerical simulation, and interactive visualization. For an MA-level course such as Economics 701 at Hunter College, the challenge for the instructor lies in augmenting the theoretical foundations found in Nicholson and Snyder’s *Microeconomic Theory* or Hal Varian’s *Intermediate Microeconomics* with tools that empower students to operationalize abstract concepts. This report provides a comprehensive analysis of available Jupyter notebooks, software toolboxes, and syllabi designed to support advanced undergraduate and graduate microeconomic instruction, specifically focusing on Python and MATLAB applications.

## The Evolution of Computational Pedagogy in Economics

The traditional approach to teaching microeconomic theory often relies on "pencil-and-paper" exercises that, while rigorous, frequently limit students to simplified functional forms that yield closed-form solutions. The introduction of computational tools like Python and MATLAB allows for the exploration of non-linear models, the visualization of complex comparative statics, and the resolution of constrained optimization problems that are algebraically intractable. Evidence from recent pedagogical research indicates that complementing traditional lectures with simulations helps students understand the subtle implications and insights of economic models, particularly when they are encouraged to experiment with parametric shifts.

At the MA level, students must bridge the gap between intermediate intuition and PhD-level technicality. This necessitates a curriculum that not only teaches theory but also equips students with marketable programming skills used in tech companies and data analysis roles. The choice of programming environment—Python, MATLAB, R, or Julia—often depends on the specific strengths of each language relative to the desired learning outcomes. Python is frequently cited as the ideal introductory language for economics due to its readability, open-source nature, and vast library ecosystem. MATLAB remains a staple in research-heavy environments that require advanced mathematical modeling and polished visualization, while Julia is gaining traction for high-performance global non-linear solution techniques.

The following table summarizes the comparative strengths of these computational tools as they relate to the microeconomic classroom environment:

| **Feature**        | **Python**                                            | **MATLAB**                                             | **R**                                   | **Julia**                                      |
| ------------------ | ----------------------------------------------------- | ------------------------------------------------------ | --------------------------------------- | ---------------------------------------------- |
| **Accessibility**  | Free, open-source, and browser-based via Google Colab | Commercial license required; robust university support | Free and open-source; statistical focus | Free and open-source; high-speed performance   |
| **Core Libraries** | NumPy, SciPy, Matplotlib, SymPy                       | Optimization, Financial, and Economics Toolboxes       | ggplot2, tidyverse, quantreg            | Optim.jl, JuMP, Plots.jl                       |
| **Primary Use**    | General purpose, data science, and modeling           | Matrix manipulations and research simulations          | Statistical analysis and econometrics   | Large-scale non-linear dynamic systems         |
| **Learning Curve** | Gentle; intuitive for beginners                       | Moderate; requires matrix-thinking                     | Moderate; specialized statistical logic | Moderate to steep; designed for high-end users |



## Quantitative Frameworks and Open-Source Curricula

For an instructor looking to expand beyond simple notebooks, several mature open-source projects provide comprehensive curriculum materials. These resources often include ready-made Jupyter notebooks that map directly to advanced theory.

### The QuantEcon Initiative

QuantEcon is perhaps the most significant resource for contemporary economic modeling. Founded by Thomas Sargent and John Stachurski, it offers an exhaustive series of lectures and notebooks for Python, Julia, and JAX. The "Intermediate Quantitative Economics with Python" and "Introduction to Economic Modeling and Data Science" series are particularly relevant for Economics 701. These materials cover linear algebra, statistics, and dynamic programming, which are critical for the "Mathematical Foundations" portion of the Nicholson textbook.

One of the standout features of the QuantEcon repository is its treatment of constrained optimization. It provides detailed notebooks on consumer theory, using the Cobb-Douglas utility function $U(B, A) = B^{\alpha}A^{1-\alpha}$ to demonstrate how to visualize indifference curves in 3D and as contour maps. These notebooks transition from manual derivation to numerical optimization using `scipy.optimize.minimize_scalar`, teaching students how to reformulate a constrained problem into an unconstrained one—a skill central to graduate theory.

### Masanori Kuroki’s Pedagogical Contributions

Masanori Kuroki has published extensively on using Python and Google Colab specifically for undergraduate and intermediate microeconomics. His work, often featured in the *International Review of Economics Education* and the *Journal of Economics Teaching*, provides clear, replicable code for utility maximization and profit maximization. Kuroki’s approach focuses on fostering intuitive understanding through minimal coding, which is ideal for students who may be new to programming.

Kuroki also explores advanced topics such as duopoly simulations that integrate advertising as a decision variable. This allows for the study of price and advertising competition, where firms face complex demand functions like $q_1 = a - bp_1 + cp_2 + dA_1^f - eA_2^g$. By using the SymPy library for symbolic math, students can solve for Nash equilibrium values of $p$ and $A$ without the burden of intense algebraic manipulation, allowing them to focus on the strategic implications of the model.

### The CompEcon Legacy and Python Ports

For instructors who prefer the rigor of computational economics as defined by Mario Miranda and Paul Fackler, the CompEcon Toolbox is an essential resource. Originally developed for MATLAB to accompany *Applied Computational Economics and Finance*, the toolbox includes routines for root-finding, optimization, and dynamic programming. Randall Romero has developed a Python version of the CompEcon toolbox that replicates this functionality in an object-oriented framework.

Romero’s Python notebooks include Cournot duopoly models with quadratic costs and Chebyshev basis function interpolation for non-linear supply and demand systems. These materials are highly suitable for an MA-level theory course because they move beyond simple linear models to address the global non-linear solution methods that dominate modern research.

## Mapping Computational Tools to Nicholson and Varian

The core chapters of Nicholson and Snyder’s *Microeconomic Theory* and Varian’s *Intermediate Microeconomics* can be systematically augmented with online software and notebooks.

### Consumer Theory and Choice Under Uncertainty

Consumer theory in Nicholson (Chapters 3-6) and Varian (Chapters 2-10) centers on preference axioms, utility functions, and the budget constraint. Mohammad Javad Goodarzi’s "Advanced Microeconomics" repository (Fall 2024) contains specific notebooks for analyzing the rationality of Cobb-Douglas and Leontief preferences, as well as the five sessions dedicated to rational axioms. These notebooks provide a computational way to test whether a set of preferences satisfies the axioms of rational choice.

For choice under uncertainty (Nicholson Chapter 7, Varian Chapter 12), Goodarzi’s notebooks explore risk preferences and the applications of uncertainty, which complement QuantEcon’s lectures on expected utility and the "Cake Eating Problem" for intertemporal choice. Christopher Carroll’s notes on "Solving Microeconomic Dynamic Stochastic Optimization Problems" also provide advanced tools for these topics, offering code in Mathematica, MATLAB, and Python.

### Production, Costs, and Market Structure

Nicholson’s treatment of production and costs (Chapters 9-12) and Varian’s firm theory (Chapters 18-22) can be operationalized using standard optimization libraries. The FIU syllabus by Alfonso details a course that uses SymPy for symbolic algebra and SciPy for constrained optimization, specifically targeting common economic models like the IS-LM and market models with government regulation.

The "Theory of the Firm" notebooks in the QuantEcon and Romero repositories allow students to visualize isoquants, expansion paths, and long-run cost curves. More specialized models, such as those addressing monopoly behavior and the impacts of market power (Nicholson Chapter 14, Varian Chapters 24-25), are addressed through interactive progression graphs in the Norton MindTap digital solution accompanying the 12th edition of Nicholson.

The table below maps the primary sections of these textbooks to relevant computational resources:

| **Textbook Topic**        | **Nicholson Chapters (12e)** | **Varian Chapters (9e)** | **Relevant Computational Resource**               |
| ------------------------- | ---------------------------- | ------------------------ | ------------------------------------------------- |
| **Mathematics for Micro** | Chapter 2                    | Chapter 1                | QuantEcon Linear Algebra; SymPy Basics            |
| **Consumer Theory**       | Chapters 3-6                 | Chapters 2-10            | Goodarzi Rational Axioms; QuantEcon Optimization  |
| **Uncertainty**           | Chapter 7                    | Chapter 12               | Carroll DSOP Notes; Goodarzi Uncertainty          |
| **Production and Costs**  | Chapters 9-12                | Chapters 18-22           | Romero CompEcon Firm Supply; Kuroki Profit Max    |
| **Perfect Competition**   | Chapter 13                   | Chapters 23-24           | Alfonso SciPy Market Model                        |
| **General Equilibrium**   | Chapter 16                   | Chapters 31-32           | Ken Judd CompEcon Course; QuantEcon Cass-Koopmans |
| **Strategic Interaction** | Chapter 8                    | Chapters 28-29           | CMU 15-326 Computational Micro; Kuroki Duopoly    |



## Institutional Precedents and Advanced Syllabi

Understanding how peer institutions structure their computational microeconomics courses provides a blueprint for expanding the curriculum at Hunter College.

### Carnegie Mellon University: Computational Microeconomics

The course 15-326 at Carnegie Mellon, titled "Computational Microeconomics," serves as an intermittent but highly influential model. Taught by faculty like Tuomas Sandholm, it uses computational techniques to operationalize concepts such as expressive marketplaces (combinatorial auctions and exchanges), game theory (equilibrium notions), and mechanism design. The syllabus draws heavily from the book *Multiagent Systems* by Shoham and Leyton-Brown and includes programming assignments in MathProg and other modeling languages.

This curriculum is particularly relevant for MA students interested in market design and the algorithmic aspects of economics. It includes specific materials on linear and integer programming, winner determination problems in auctions, and the computation of Nash equilibria in both normal and extensive-form games.

### Rice University and Stanford: High-Level Integration

Rice University offers a Master of Computational Economics program with specific courses like ECON 632 ("Data Tools for Computational Economics") and ECON 633 ("Dynamic Models for Computational Economics"). These courses utilize Python’s core scientific libraries—NumPy, SciPy, Matplotlib, and Pandas—to handle messy datasets, construct informative visualizations, and implement dynamic programming and Markov models.

Stanford University’s computational economics course, famously associated with Ken Judd, introduces students to numerical analysis and approximation theory as a precursor to solving economic models. Judd’s approach emphasizes that doing computation is the only way to learn computation, a philosophy reflected in the weekly computational exercises and term projects assigned in his course. The materials include solution techniques for ordinary and partial differential equations and perturbation methods useful in dynamic economic analysis.

### Hunter College Context: The Syllabi Directory

Hunter College students and the Hunter Open Source Club maintain a directory of syllabi that, while currently focused on Computer Science and Philosophy, demonstrates a growing institutional culture of resource sharing. The directory serves as a repository for syllabi and faculty mugshots, advocating for open APIs and tools to improve student life. Leveraging this existing infrastructure to host and share Economics 701 materials could enhance departmental visibility and collaboration within the CUNY system.

## Advanced Optimization and Numerical Techniques

For an MA-level theory class, the depth of optimization must go beyond the basic Lagrangian. Students should be introduced to the Karush-Kuhn-Tucker (KKT) conditions and duality theory, which are essential for handling inequality constraints and understanding the economic meaning of shadow prices.

### Python and MATLAB for Constrained Optimization

In Python, the `scipy.optimize` library provides the `minimize` function, which supports various methods for constrained optimization, such as SLSQP and COBYLA. Notebooks from the Allameh Tabataba’i University course show sessions specifically dedicated to the numerical verification of KKT conditions. Similarly, MATLAB’s Optimization Toolbox is frequently used in graduate courses to solve linear and non-linear programming problems, providing a robust environment for verifying first and second-order optimality conditions.

The QuantEcon toolkit provides a bridge between these two worlds, often referencing MATLAB-style IDEs like Spyder alongside the Jupyter notebook interface. This allows students who are familiar with one environment to transition smoothly to the other. Furthermore, advanced toolkits like JAX allow for automatic differentiation and GPU-accelerated optimization, which is becoming increasingly relevant for high-dimensional economic models.

### Symbolic Mathematics with SymPy

A common hurdle for graduate students is the algebraic complexity of first-order conditions in models with many variables. SymPy allows students to define variables as symbols and perform differentiation, integration, and equation solving programmatically. For example, in a duopoly advertising model, a student can define the profit functions symbolically and use `sp.solve` to find the equilibrium reaction functions. This pedagogical technique allows the class to focus on the "Second-Order Insights"—such as how changes in advertising elasticity affect the equilibrium markup—rather than getting lost in the calculus.

## Dynamic Modeling and Recursive Methods

A significant portion of graduate microeconomic theory focuses on how economic variables evolve over time. This requires an understanding of dynamic programming and stochastic processes.

### Dynamic Programming Notebooks

The QuantEcon series provides exhaustive notebooks on dynamic programming, covering both discrete and continuous state and action variables. Key notebooks include:

- **Policy Iteration and Value Function Iteration:** These notebooks demonstrate the rate of convergence between different algorithms and their applications to inventory dynamics and optimal growth models.
- **The Endogenous Grid Method (EGM):** A notebook specifically focused on this efficient numerical technique used to solve microeconomic consumption-savings models.
- **Structural Estimation:** Notebooks on the Rust-Zurcher model of machine replacement, which bridge the gap between theory and structural econometrics.

These resources align with the "Extensions" found in Nicholson, such as those addressing computable general equilibrium (CGE) models and intertemporal choices.

### Stochastic Processes and Risk

Understanding risk aversion requires simulating stochastic demand or income shocks. The CompEcon toolbox for MATLAB and its Python version include solvers for discrete time/discrete variable dynamic programming (Markov Chains) and solvers for financial asset pricing. These tools allow students to simulate the downside risks, including market and liquidity risks, in a portfolio or consumption model. Christopher Carroll’s HARK Framework (a supercessor to his original notebooks) is another powerful Python library designed specifically for solving microeconomic dynamic stochastic optimization problems.

## Practical Implementation and Suggestion for Economics 701

To effectively expand the Economics 701 curriculum, several strategies can be employed to integrate these software materials into the existing course structure.

### Ideas for Interactive Problem Sets

1. **Rationality Check:** Instead of a traditional problem, have students write a script to test if a given set of consumer choices satisfies the Weak Axiom of Revealed Preference (WARP). Mohammad Javad Goodarzi’s notebooks provide a clear template for this.
2. **Duopoly Advertising Simulation:** Use Masanori Kuroki’s framework to have students simulate a duopoly where firms compete in both price and advertising. Students can vary parameters like own-price elasticity versus cross-advertising effects to see how the equilibrium shifts.
3. **Visualizing the Edgeworth Box:** Use the interactive graphs from EconGraphs (Makler) or the Wolfram Demonstrations Project to let students manipulate endowments and see the contract curve move in real-time.
4. **Shadow Prices in Linear Programming:** Use QuantEcon’s linear programming notebooks to solve a simple production problem. Have students interpret the "shadow price" of a constraint and compare it to the market price of the resource.

### Software Deployment Strategies

For the Fall 2026 term, the use of Google Colab is highly recommended for assignment distribution. Because it is cloud-hosted and requires no 프로젝트 setup, it allows the instructor to spend more time on course content and less on technical troubleshooting. Integrating GitHub Classroom can further streamline the workflow, allowing for automated project status updates and submissions.

For students who prefer a more traditional programming environment, the Anaconda distribution provides an all-in-one installation of Python, Jupyter, and the Spyder IDE, the latter of which provides a familiar interface for those coming from a MATLAB background.

### Leveraging Commercial Digital Solutions

In addition to open-source materials, the instructor may consider the Norton Illumine Ebook and Smartwork online problem sets that accompany the Varian and Nicholson texts. These platforms include thorough Varian content with engaging animations and interactive workbooks authored by Marc Melitz. These tools provide a low-stakes environment for students to practice problem-solving before moving on to the more complex Python-based simulations.

## Strategic Syllabi Mapping and Learning Goals

The integration of computational tools should serve clearly defined learning goals. According to syllabi from peer institutions, these goals typically include:

1. **Analytical Tool Mastery:** Applying calculus, optimization, and graphs to rigorously analyze decision-making under constraints.
2. **Market Outcome Analysis:** Modeling consumer and producer choices mathematically to evaluate efficiency and welfare across different market structures.
3. **Technological Proficiency:** Developing basic familiarity with the Python scientific computing stack (NumPy, SciPy, Matplotlib, Pandas) and the use of Jupyter notebooks.
4. **Scientific Reproducibility:** Learning to use version control and well-documented code to ensure that economic findings are transparent and replicable.

The following table provides a comprehensive overview of the online software materials and their associated websites:

| **Resource Name**        | **Primary Platform** | **Target Level**   | **Website/Repository**                                       | **Key Features**                                             |
| ------------------------ | -------------------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **QuantEcon**            | Python, Julia, JAX   | Undergrad to PhD   | [quantecon.org](https://quantecon.org/)                      | Comprehensive dynamic programming and optimization lectures  |
| **CompEcon (Python)**    | Python               | Graduate           | [github.com/randall-romero/CompEcon](https://github.com/randall-romero/CompEcon) | Object-oriented port of Miranda-Fackler MATLAB toolbox       |
| **EconGraphs**           | Interactive Web      | Undergraduate      | [econgraphs.org](https://econgraphs.org/)                    | 350+ interactive graphs for consumer and firm theory         |
| **Advanced Micro (F24)** | Python               | Master’s           | [github.com/mjavadg/Advanced-Microeconomics_Fall2024](https://github.com/mjavadg/Advanced-Microeconomics_Fall2024) | Focus on preference axioms and uncertainty                   |
| **Kuroki Repositories**  | Python (Colab)       | Undergraduate / MA | (https://doi.org/10.1016/j.iree.2021.100225)                 | Replicable profit and utility maximization code              |
| **HARK Framework**       | Python               | Graduate           | [econ-ark.org](https://econ-ark.org/)                        | Advanced stochastic dynamic optimization for life-cycle models |
| **Norton Illumine**      | Web / Ebook          | Undergraduate      | [seagull.wwnorton.com](https://seagull.wwnorton.com/)        | Commercial interactive animations and problem sets for Varian |
| **CompEcon (MATLAB)**    | MATLAB               | Graduate           | [pfackler.wordpress.ncsu.edu/compecon](https://pfackler.wordpress.ncsu.edu/compecon) | The original toolkit for computational economics             |



## Future Outlook and Emerging Themes

As Economics 701 moves toward Fall 2026, the inclusion of "Machine Learning for Economics" and "Artificial Intelligence in Mechanism Design" is likely to become more prominent in MA-level syllabi. Institutions like Rice and Carnegie Mellon are already integrating these topics into their computational curriculum. This includes using reinforcement learning for inventory management (via Q-learning) and supervised learning for predicting market outcomes.

The transition toward cloud-based collaborative coding and open-source software not only improves the student learning experience but also aligns the Hunter College MA program with global trends in economic research. By utilizing a mix of advanced toolboxes like CompEcon and pedagogical notebooks like those from Kuroki and QuantEcon, the Economics 701 course can provide a rigorous, modern, and highly relevant education in microeconomic theory. The strategic use of Google Colab and GitHub Classroom will further ensure that students are prepared for the technical demands of the future economic job market.