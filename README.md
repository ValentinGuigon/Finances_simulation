RAJOUTER:
- Possibilité de dual traks: En gros on dit que le compute_gains y'a une fonction pour des investissements et il manque des fonctions pour:
    * retraite d'état USA, qui fera une petite track parallèle avant de rejoindre le reste. ???
- compte-rendu numérique: trouver de meilleures metrics?
- transactions (enlever et remettre)
- faire des simulations en termes de stratégies
- utiliser du java ou autre pour visualiser en html
- rajouter un genre de GUI?

- disparition d'un livret
- pourquoi pas trouver un index de la fiscalité selon le pays et donc le prendre automatiquement quand on choisi le pays
- mettre les nouveaux paramètres dans "get_update_parameters"
- mettre les init_states et update_states dans un script commun ?
- choisir les banques 
- transferts interbancaires avec tarifs 
- possibilité de demander un prêt avec intérêt remboursement et tout
- définir une track immobilier
- pour chaque track (investissement, épargne, income, immobilier), définir la possibilité d'avoir plusieurs sources et de les nommer
Et comment on fait pour le csv dans ces cas ?
- dans transactions pouvoir demander prêt, rembourser, bouger assets, vendre maison
- update les graphs en fonction
- quoi d'autre ?

Avoir des paramètres en défaut mais au lancement lancer un GUI pour demander si définition à la mano des paramètres
Si oui, ouvre un menu avec tous les params: prendre la valeur donnée si existe, sinon prendre valeur par défaut 

# We are now going to set up a whole model for creating a personal portfolio with wealth simulation:

1. Set our basic inflow, starting assets, taxes and income raises
2. Download historic S&P 500 index prices 
    a. We download the S&P500
    b. We calculate the average monthly return and standard deviation of a chosen historic period
    c. We store these values to use later as inputs to our Standard Normal distribution (The values are coming out as a monthly return of 0.6% and a monthly volatility (standard deviation) of 4.15%.)
3. Calculate income (with taxation)
4. Calculate outflows (including preparing retirement) and subtract them from the income
5. Generate a monthly market return by drawing from the normal distribution with taxation on investment gains
6. Generate a monthly savings return
7. Allocate the remaining income (priority to savings then to market)
8. Calculate the end of period assets value
9. Output graphs
10. Output metrics


## Notes on the S&P
When we plot our series of investment returns we can see that they are indeed stochastic in nature, with the inherent randomness of returns meaning some months we are up, some we are down even though our average monthly return used as an input to the Standard Normal function was positive. 
As a slight point to note – please be aware that some of the plots are showing the series of cumulative monthly investment returns, whereas some of them are showing the series of ending period asset value – they are different things!
We have modelled our monthly active salary (with an annual percentage increase), along with our monthly investment returns which we have subjected to a stochastic element to mimic the real-world.


# Notes on investment failures
The code allowed for a situation where we go could “bust”, losing everything we have in terms of investable assets, and continue “investing” a negative amount. 
This is obviously nonsensical as you cant make positive returns from a negative asset base, just because the market returns are negative. We will add a flag that checks to make sure our asset base is in positive territory before we start calculating and applying investment returns; if our asset base is negative, there are a few things we can do to ac count for that – 

Just for example we could:
* Consider that situation “unnaceptable” to the extent we class ourselves as “ruined/bankrupt” and end the simulation with a “failure” flaf or label.
* Allow the simulation to continue and collect salary income each month, but each month where assets are non-positive, we set the investment gains to zero by default.
* Apply some non-trivial logic that applies interest and penalty charges, allow us to borrow and re-invest etc.

The last option, is just not realistic nor really the point of this exercise. We go for option 1, considering an asset base of zero to be unacceptable and a sign of abject failure with regards to money management and such. 
You could even argue that even getting close to a zero value asset base is unacceptable and want to set the “failure” threshold somewhere above zero. We can revisit these options later perhaps if it is of benefit.

We deal with a failed simulation by recording a “failure flag” – mark that run as failed for later analysis. This reasoning will become a bit clearer later on when we start to apply Monte Carlo methods to our model, carrying out 100s, 1000s or more simulations per “experiment”.


# Notes on retirement
We set a future date at which we plan to retire and effectively cease working, with the accompanying expectation that our active income (i.e. salary) will fall dramatically, if not disappear altogether. 

Retirement is an important stage of life to plan for; not only would our inflows from salary be affected, it is likely many of our outflows would change too. 
By retirement age, it is not uncommon for people to have paid off any outstanding mortgage debt on their homes. This means no more monthly mortgage outflows, and offers other opportunities such as equity release schemes, or “downsizing” of property etc.
In other words, both our post-retirement inflows and outflows are usually fundamentally different from the “normal”, non-retirement situation. For instance, we no longer pay rent or mortgage payments. We could also imagine our health insurance costs and general medical expenses would rise significantly on average, and we might start to receive some pension income each month

**Of utmost importance is to ensure that by the time you retire, you have built an asset base large enough to sustain your needs and generate enough investment income to cover your living costs, for however many years you end up living in retirement.**

Indeed, we can sometimes observe the effect our drop in salary after retirement has on our ending asset values through time. With no salary coming, there is the tendency for our personal wealth and asset base to fall over time. 

## Getting Started
Step 1: Set a Realistic Retirement Income Goal
Determine the amount of money you wish to have as annual income after retirement. For instance, if your goal is 3,000 $ per month, this equates to 36,000 $ per year.

Step 2: Consider the Impact of Inflation
Recognize the effect of inflation on your future purchasing power. Adjust your retirement income goal accordingly, taking into account a realistic inflation rate. For instance, a 3% annual inflation rate implies that the value of money will decrease over time.

Step 3: Calculate the Required Retirement Fund
Assuming a certain interest rate on your investments (e.g., 5% per year), use the formula: 
Retirement Fund = Annual Income / Interest Rate
This calculation helps you determine the total amount needed in your retirement fund to generate the desired annual income.

Step 4: Long-Term Investment Planning
Estimate the annual investment required to reach your retirement fund goal. This involves factoring in the desired retirement fund, expected return on investment, and adjustments for inflation.