import numpy as np
import pandas as pd
from IPython.display import display
from scipy import stats
from statsmodels.stats.power import TTestIndPower

class DatasetHelper:
    """
    Hjälpklass för att läsa in och förhandsgranska ett dataset med pandas.
    
    Attributes:
        file_path (str): Sökväg till CSV-filen.
        df (pd.DataFrame): DataFrame som lagrar datasetet efter inläsning.
    """
    def __init__(self, file_path):
        """
        Initierat klassen med filens sökväg
        """
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """
        Läser in CSV-filen till en pandas DataFrame
        """
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Data laddades från {self.file_path}")
        except Exception as e:
            print(f"Fel när datan laddades: {e}")
    
    def preview(self, n=5):
        """
        Visar de första raderna i datasetet
        """
        if self.df is not None:
            display(self.df.head(n))
        else:
            print("Datan har inte laddats än. Använd load_data() först.")

    def summary(self):
        """
        Visar beskrivande statistik för datasetet.
        """
        if self.df is not None:
            display(self.df.describe())
        else:
            print("Datan har inte laddats än. Använd load_data() först.")
    
    def info(self):
        """
        Visar info om datasetet
        """
        if self.df is not None: 
            display(self.df.info())
        else:
            print("Datan har inte laddats än. Använd load_data() först.")

    def missing_values(self):
        """
        Visar antal saknade värden per kolumn
        """
        if self.df is not None:
            display(self.df.isna().sum())
        else:
            print("Datan har inte laddats än. Använd load_data() först.")


class HealthSimulator:
    """
    En enkel klass för att beräkna den verkliga andelen av en sjukdom i ett dataset,
    simulera nya observationer baserat på dessa sannolikheter och jämföra verkliga och
    simulerade andelar.

    Parametrar
    ----------
    df : pandas.DataFrame
        Dataset innehållande en kolumn för "disease" och valfri gruppkolumn.
    disease_col : str, default="disease"
        Kolumnnamn anger sjukdomsstatus (0/1).
    group_col : str or None, default="sex"
        Kolumnen används för att gruppera andelar. Om None, ingen gruppsimulation. 
    random_state : int eller None, default=None
        Seed för att reproducera simulationer. 
      """
    
    def __init__(self, df, disease_col="disease", group_col="sex", random_state=None):
        self.df = df
        self.disease_col = disease_col
        self.group_col  = group_col
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)

        self.true_proportion = None
        self.true_group_proportion = None
        self.sim_total = None
        self.sim_groups = None

    def compute_true_proportions(self):
        """Beräknar verkliga andelar (total och per grupp)"""
        disease = self.df[self.disease_col]
        
        # Räknar den verkliga andelen
        self.true_proportion = disease.mean()

        # Räknar andelar per grupp
        if self.group_col is not None:
            self.true_group_proportion = self.df.groupby(self.group_col)[self.disease_col].mean()
        else: self.true_group_proportion = None

    def simulate(self, n=1000):
        """Simulerar binära sjukdomsutfall baserat på de verkliga andelarna."""
        if self.true_proportion is None:
            self.compute_true_proportions()

        # Total simulering
        p = self.true_proportion
        self.sim_total = self.rng.choice([0, 1], size=n, p=[1-p, p])

        # Gruppsimuleringar
        if self.true_group_proportion is not None:
            self.sim_groups = {}
            for group, prop in self.true_group_proportion.items():
                self.sim_groups[group] = self.rng.choice([0, 1], size=n, p=[1-prop, prop])
        else: 
            self.sim_groups = None

    def print_report(self):
        """Skriver ut verkliga andelar, simulerade andelar och skillander"""
        print("Verkliga andelar")
        print("=========================================")
        print(f"Andelen med sjukdomen:              {self.true_proportion:.1%}")

        if self.true_group_proportion is not None: 
            for g, p in self.true_group_proportion.items():
                print(f"Andel {g} med sjukdom:                {p:.1%}")
        
        print("\nSimulerade andelar") 
        print("=========================================")  
        print(f"Simulerad andel med sjukdom:        {self.sim_total.mean():.1%}")

        if self.sim_groups is not None:
            for g, arr in self.sim_groups.items():
                print(f"Simulerad andel {g}:                  {arr.mean():.1%}")
        
        print("\nJämförelse")
        print("=========================================") 
        diff_total = abs(self.sim_total.mean() - self.true_proportion) 
        print(f"Total skillnad:                     {diff_total:.2%}")

        if self.sim_groups is not None:
            for g in self.true_group_proportion.index:
                diff = abs(self.sim_groups[g].mean() - self.true_group_proportion[g])
                print(f"Skillnad {g}:                         {diff:.1%}")
                
class ConfidenceIntervalCalculator:
    """
    Beräknar konfidensintervall för medelvärde med normalapproximation och bootstrap

       Parametrar
    ----------
    data : array-like
        En lista, array eller pandas-kolumn med numeriska värden.
    confidence : float, valfri
        Konfidensnivån, t.ex. 0.95 för 95 % intervall. Standard är 0.95.
    n_bootstrap : int, valfri
        Antal bootstrap-replikat som ska genereras. Standard är 10000.
    random_state : int, valfri
        Slumpfrö för reproducerbarhet.
    """
    def __init__(self, data):
        """Iniitiera med en pandas- eller numpy-serie."""
        self.data = np.array(data.dropna())
        self.n = len(self.data)
        self.mean = self.data.mean()
        self.std = self.data.std(ddof=1)
        self.se = self.std / np.sqrt(self.n)

    def normal_ci(self, z=1.96):
        """Beräknar 95%-CI med normalapproximation"""
        lower = self.mean - z * self.se
        upper = self.mean + z * self.se
        return lower, upper
    
    def bootstrap_ci(self, n_boot=10_000, ci=95):
        """Beräkna 95%-CI med bootstrap"""
        boot_means = []
        for _ in range(n_boot):
            sample = np.random.choice(self.data, size=self.n, replace=True)
            boot_means.append(sample.mean())

        boot_means = np.array(boot_means)
        alpha = (100 - ci) / 2
        lower = np.percentile(boot_means, alpha)
        upper = np.percentile(boot_means, 100 - alpha)
        return lower, upper
    
    def print_report(self):
        """Skriver ut resultat för konfidensintervall"""
        ci_norm = self.normal_ci()
        ci_boot = self.bootstrap_ci()

        print(f"Punktestimat (medelvärde):    {self.mean:.1f} mmHg")
        print(f"Standardfel:                  {self.se:.3f} mmHg")
        print("=====================================")
        print(f"95% CI (normalapproximation): [{ci_norm[0]:.1f}, {ci_norm[1]:.1f}] mmHg")
        print(f"95% CI (bootstrap):           [{ci_boot[0]:.1f}, {ci_boot[1]:.1f}] mmHg")

class HypothesisTester: 
    """
    Utför Welch’s t-test, beräknar effektstorlek och power mellan två grupper.

    Parametrar
    ----------
    group1 : array-like
        Numeriska värden för grupp 1 (t.ex. rökare).
    group2 : array-like
        Numeriska värden för grupp 2 (t.ex. icke-rökare).
    """
    def __init__(self, group1, group2):
        self.group1 = np.array(group1)
        self.group2 = np.array(group2)

        # Resultatet lagras här efter körning
        self.means = {}
        self.t_stat = None
        self.p_two_sided = None
        self.p_one_sided = None
        self.effect_size = None
        self.power_two_sided = None
        self.power_one_sided = None

    def compute_test(self):
        """Kör Welch's t-test och beräknar p-värden."""
        # Medelvärden
        self.means["group1"] = self.group1.mean()
        self.means["group2"] = self.group2.mean()

        # Welch's t-test
        self.t_stat, self.p_two_sided = stats.ttest_ind(
            self.group1, self.group2, equal_var=False
        )

        #Ensidigt p-värde
        if self.means["group1"] > self.means["group2"]:
            self.p_one_sided = self.p_two_sided / 2
        else:
            self.p_one_sided = 1 - self.p_two_sided / 2

    def compute_effect_size(self):
        """Beräknar Cohen's d för två oberoende grupper."""
        std1 = self.group1.std(ddof=1)
        std2 = self.group2.std(ddof=1)
        pooled_std = np.sqrt((std1 ** 2 + std2 ** 2) / 2)

        self.effect_size = (self.means["group1"] - self.means["group2"]) / pooled_std

    def compute_power(self, alpha=0.5):
        """ Beräknar power för tvåsidigt och ensidigt test."""
        analysis = TTestIndPower()

        n1 = len(self.group1)
        n2 = len(self.group2)
        ratio = n2 / n1

        self.power_two_sided = analysis.power(
            effect_size=self.effect_size,
            nobs1=n1,
            ratio=ratio,
            alpha=0.5,
            alternative="two-sided"
        )
        
        self.power_one_sided = analysis.power(
            effect_size=self.effect_size,
            nobs1=n1,
            ratio=ratio,
            alpha=0.5,
            alternative="larger"
        )

    def print_report(self):
        """Skriver ut resultat för hypotesprövningen"""
        print("=====================================")
        print(f"Medelvärde grupp 1:   {self.means['group1']:.2f} mmHg")
        print(f"Medelvärde grupp 2:   {self.means['group2']:.2f} mmHg")

        print("=====================================")
        print(f"t-värde:              {self.t_stat:.3f}")
        print(f"p-värde (tvåsidigt):  {self.p_two_sided:.3f}")
        print(f"p-värde (ensidigt):   {self.p_one_sided:.3f}")

        print("=====================================")
        print(f"Cohen's d:            {self.effect_size:.3f}")

        print("=====================================")
        print(f"Power (tvåsidigt):    {self.power_two_sided:.3f}")
        print(f"Power (ensidigt):     {self.power_one_sided:.3f}")
        print("=====================================")