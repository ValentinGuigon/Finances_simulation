# Getting Started

1. Step 1: Choose your parameters
Model parameters are approximations based from my experience as a French citizen. Please modify the parameters as you wish in *get_parameters.py*.

2. Step 2: Calculate the Required Retirement Fund
Choose the amount you wish to decude from your assets as monthly pension in *predict_retirement.py*

3. Step 3: Long-Term Investment Planning
Given the metric and graphical outputs from the assets modeling and the retirement modeling, adjust your planning


## Notes on the modelling

- Set a Realistic Retirement Income Goal
Determine the amount of money you wish to have as annual income after retirement. For instance, if your goal is 3,000 $ per month, this equates to 36,000 $ per year.

- Consider the Impact of Inflation
Recognize the effect of inflation on your future purchasing power. Adjust your retirement income goal accordingly, taking into account a realistic inflation rate. For instance, a 3% annual inflation rate implies that the value of money will decrease over time.

- Compute the Required Retirement Fund wisely
Assuming a certain interest rate on your investments (e.g., 5% per year), use the formula: 
Retirement Fund = Annual Income / Interest Rate
This calculation helps you determine the total amount needed in your retirement fund to generate the desired annual income.

- Mind the known unknown variables and the unknown unknown variables
Estimate the annual investment required to reach your retirement fund goal. This involves factoring in the desired retirement fund, expected return on investment, and adjustments for inflation.



# Mechanics of the simulation
Here are the steps behind the whole model. They support the creating a personal portfolio with wealth simulation but beware of potential mistakes in the coding

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
11. Feed the results to the retirement simulation
12. Outputs metrics for failure rate of the retirement plan
13. Outputs graphs
14. Please adjust your expectations


## Notes on the model assumptions
### 1. ETF assumption
The model computes the returns based on trends from a single market - for instance S&P500. 
It doesn't permit yet the computation of single assets with each their own risk/return.
The model therefore makes the assumption that assets are computed **a)** from a tracker ETF, that tracks a whole market, and **b)** without going through a financial professional.

a) These passive ETFs (*trackers*) track a financial index as closely as possible, unlike other forms of collective investment that attempt to beat a benchmark index.
The reason is that modern finance has come to the conclusion that taking risk in a diversified way yields a certain return over the long term. The expectation of this return is proportional to the degree of risk taken. The more risk you take by being diversified, the higher the return you can expect after a few years. 

b) The question then arises: why not invest in a diversified way through a financial professional? Why follow a stock market index?
On average, professional managers match the performance of index ETFs, when fees are not taken into account. 
When management fees and, above all, transaction costs are taken into account, actively managed investment funds underperform ETFs, since an index ETF generally charges 5 to 15 times less in fees than an actively managed fund. Index management is much more passive and does not move the portfolio very much, so generates few transaction costs.

- **The most profitable investment logic for a rational investor is free index investing, with the lowest possible fees**.
- There are exceptions in opaque financial markets with large information asymmetries, such as micro-cap equities and high-yield bonds, where active management is more attractive.

Source: [Pace, Hili and Grima - 2016: Active versus passive investing: An empirical study on the US and European mutual funds and ETF](https://www.um.edu.mt/library/oar/bitstream/123456789/19202/1/Chapter%20-%20Active%20versus%20Passive%20Investing%20%20An%20Empirical%20Study%20on%20the%20US%20and%20European%20Mutual%20Funds%20and%20ETFs.pdf)

#### Notes on physical vs synthetic replication
* A physical/direct ETF invests directly in the securities of the index it is designed to replicate.
    * When the ETF invests in all the securities in the index, we speak of *full replication*.
    * If it invests only in the securities with the highest weight, those that are the most liquid or with other considerations that cause it to deviate from the index, it is referred to as *sampling replication*.
* A synthetic ETF is designed to replicate the return of a selected index (e.g., S&P 500 or FTSE 100) just like any other ETF. But instead of holding the underlying securities or assets, they use financial engineering to achieve the desired results.

What's the right choice between physical and synthetic replication? What are the risks involved?
* Often, in France, there is no choice, as in the case of PEA ETFs that replicate non-EEA indices.
* If you do have a choice, synthetic replication is, on average, much more faithful to the index than physical replication for the same assets and index. However, synthetic replication is more complex to understand, and if you don't understand it, you're better off investing in physical replication.
* Both methods are equivalent over the long term and present similar counterparty risks: physical replication with securities lending (completely opaque, with an underlying conflict of interest), synthetic replication with the concentration of risk on a single counterparty.

The risks associated with replication are negligible compared with the market risks of the indices being replicated.
[The underlying bet in equity investing is the bet in the stability of systemically important banks, which are behind almost all European ETFs.](https://www.fsb.org/wp-content/uploads/P211122.pdf)

[More on counterparty risk in this research paper](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3352711_code271616.pdf?abstractid=2462747&mirid=1)


## Notes on the S&P
When we plot our series of investment returns we can see that they are indeed stochastic in nature, with the inherent randomness of returns meaning some months we are up, some we are down even though our average monthly return used as an input to the Standard Normal function was positive. 
As a slight point to note – please be aware that some of the plots are showing the series of cumulative monthly investment returns, whereas some of them are showing the series of ending period asset value – they are different things!
We have modelled our monthly active salary (with an annual percentage increase), along with our monthly investment returns which we have subjected to a stochastic element to mimic the real-world.


## Notes on investment failures
The code allowed for a situation where we go could “bust”, losing everything we have in terms of investable assets, and continue “investing” a negative amount. 
This is obviously nonsensical as you cant make positive returns from a negative asset base, just because the market returns are negative. We will add a flag that checks to make sure our asset base is in positive territory before we start calculating and applying investment returns; if our asset base is negative, there are a few things we can do to ac count for that – 

Just for example we could:
* Consider that situation “unnaceptable” to the extent we class ourselves as “ruined/bankrupt” and end the simulation with a “failure” flaf or label.
* Allow the simulation to continue and collect salary income each month, but each month where assets are non-positive, we set the investment gains to zero by default.
* Apply some non-trivial logic that applies interest and penalty charges, allow us to borrow and re-invest etc.

The last option, is just not realistic nor really the point of this exercise. We go for option 1, considering an asset base of zero to be unacceptable and a sign of abject failure with regards to money management and such. 
You could even argue that even getting close to a zero value asset base is unacceptable and want to set the “failure” threshold somewhere above zero. We can revisit these options later perhaps if it is of benefit.

We deal with a failed simulation by recording a “failure flag” – mark that run as failed for later analysis. This reasoning will become a bit clearer later on when we start to apply Monte Carlo methods to our model, carrying out 100s, 1000s or more simulations per “experiment”.


## Notes on retirement
We set a future date at which we plan to retire and effectively cease working, with the accompanying expectation that our active income (i.e. salary) will fall dramatically, if not disappear altogether. 

Retirement is an important stage of life to plan for; not only would our inflows from salary be affected, it is likely many of our outflows would change too. 
By retirement age, it is not uncommon for people to have paid off any outstanding mortgage debt on their homes. This means no more monthly mortgage outflows, and offers other opportunities such as equity release schemes, or “downsizing” of property etc.
In other words, both our post-retirement inflows and outflows are usually fundamentally different from the “normal”, non-retirement situation. For instance, we no longer pay rent or mortgage payments. We could also imagine our health insurance costs and general medical expenses would rise significantly on average, and we might start to receive some pension income each month

**Of utmost importance is to ensure that by the time you retire, you have built an asset base large enough to sustain your needs and generate enough investment income to cover your living costs, for however many years you end up living in retirement.**

Indeed, we can sometimes observe the effect our drop in salary after retirement has on our ending asset values through time. With no salary coming, there is the tendency for our personal wealth and asset base to fall over time. 


# RAJOUTER:
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


# Acknowledgments

I'd like first to thank **Stuart J.** for his series on creating a personal portoflio/wealth simulation if Python. I got started by implementing his great tutorial from [Python For Finance](https://www.pythonforfinance.net/2021/06/13/create-a-personal-portfolio-wealth-simulation-in-python/)
I'd like to thank **Tony Yiu** and his series on simulating retirement. I Implemented his retirement simulation from [Towards Data Science](https://towardsdatascience.com/do-i-have-enough-money-to-retire-af7914a07b34)