# Mathematical Soundness & Proof Semantics

## 1. Formal Preliminaries

Let $\mathcal{C}$ be a countable set of constant symbols, $\mathcal{V}$ be a set of variable symbols, and $\mathcal{P}$ be a set of predicate symbols.
A **literal** $L$ is of the form $P(t_1, \dots, t_k)$ or $\neg P(t_1, \dots, t_k)$, where $P \in \mathcal{P}$ and $t_i \in \mathcal{C} \cup \mathcal{V}$.
A **rule** $R$ is a definite clause:
$$B_1 \land B_2 \land \dots \land B_m \to H$$
where $B_i$ and $H$ are literals.

### Safety Condition (Variable Binding)
A rule $R$ is **safe** if and only if:
$$\operatorname{vars}(H) \subseteq \bigcup_{i=1}^m \operatorname{vars}(B_i)$$
The `RepresentationValidator` strictly enforces this condition, rejecting any rule where $\operatorname{vars}(H) \setminus \bigcup \operatorname{vars}(B_i) \neq \emptyset$.

---

## 2. Forward Chaining Saturation

Let $\mathcal{KB} = (\mathcal{F}, \mathcal{R})$ be a knowledge base where $\mathcal{F}$ is a finite set of ground literals and $\mathcal{R}$ is a set of safe rules.
The immediate consequence operator $T_{\mathcal{R}}$ is defined as:
$$T_{\mathcal{R}}(\mathcal{S}) = \mathcal{S} \cup \{ \theta(H) \mid \exists R \in \mathcal{R}, \theta \text{ such that } \forall B \in \operatorname{body}(R), \theta(B) \in \mathcal{S} \}$$

### Theorem 1 (Termination and Fixed Point)
Since the Herbrand base $\mathcal{H}_{\mathcal{KB}}$ formed by the finite constants in $\mathcal{KB}$ is finite, the sequence:
$$\mathcal{S}_0 = \mathcal{F}, \quad \mathcal{S}_{k+1} = T_{\mathcal{R}}(\mathcal{S}_k)$$
monotonically increases ($\mathcal{S}_k \subseteq \mathcal{S}_{k+1} \subseteq \mathcal{H}_{\mathcal{KB}}$) and reaches a unique least fixed point $\mathcal{S}^* = T_{\mathcal{R}}^\infty(\mathcal{F})$ in at most $|\mathcal{H}_{\mathcal{KB}}|$ steps.

---

## 3. Three-Way Open-World Decision Procedure

For any ground query literal $Q \in \mathcal{H}_{\mathcal{KB}}$ and its classical complement $\neg Q$:

$$\operatorname{Status}(Q) = \begin{cases}
\text{ENTAILED} & \text{if } Q \in \mathcal{S}^* \land \neg Q \notin \mathcal{S}^* \\
\text{CONTRADICTED} & \text{if } Q \notin \mathcal{S}^* \land \neg Q \in \mathcal{S}^* \\
\text{CONTRADICTED (Conflict)} & \text{if } Q \in \mathcal{S}^* \land \neg Q \in \mathcal{S}^* \\
\text{UNKNOWN} & \text{if } Q \notin \mathcal{S}^* \land \neg Q \notin \mathcal{S}^*
\end{cases}$$

---

## 4. Proof Graph Soundness

A proof DAG $\mathcal{G} = (\mathcal{V}_G, \mathcal{E}_G)$ is valid with respect to $\mathcal{KB}$ if:
1. Every source node $v \in \mathcal{V}_G$ with in-degree 0 corresponds to a ground fact $F \in \mathcal{F}$ or rule $R \in \mathcal{R}$.
2. Every internal node $u \in \mathcal{V}_G$ corresponds to an inference $H$ such that $\exists R \in \operatorname{parents}(u)$ and ground premises $B_1, \dots, B_m \in \operatorname{parents}(u)$ with substitution $\theta$ satisfying $\theta(\operatorname{body}(R)) = \{B_1, \dots, B_m\}$ and $\theta(\operatorname{head}(R)) = H$.
3. $\mathcal{G}$ contains no directed cycles ($\mathcal{G}$ is a DAG).
4. The sink node $g \in \mathcal{V}_G$ corresponds to the query goal $Q$ (or $\neg Q$ under contradiction).
