export interface IngredientOutput {
  name: string;
  ingredient_id?: string | null;
  weight_kg?: number | null;
  co2_per_kg?: number | null;
  co2_kg?: number | null;
  calculation_notes?: string | null;
  weight_estimation_notes?: string | null;
  co2_emission_notes?: string | null;
  energy_kj?: number | null;
  fat_g?: number | null;
  carbohydrate_g?: number | null;
  protein_g?: number | null;
}

export interface RecipeCO2Output {
  title?: string | null;
  url: string;
  total_co2_kg: number;
  number_of_persons?: number | null;
  co2_per_person_kg?: number | null;
  avg_meal_emission_per_person_range_kg: number[];
  avg_emission_per_person_per_meal: number;
  avg_emission_per_person_per_day: number;
  budget_emission_per_person_per_meal: number;
  budget_emission_per_person_per_day: number;
  energy_per_person_kj?: number | null;
  calories_per_person_kcal?: number | null;
  fat_per_person_g?: number | null;
  carbohydrate_per_person_g?: number | null;
  protein_per_person_g?: number | null;
  ingredients: IngredientOutput[];
}

export interface Comparison {
  label: string;
  input_co2_kg: number;
  reference_co2_kg: number;
  comparison: number;
  help_text: string;
}

export interface AvgEmissionPerPerson {
  meal: number;
  day: number;
}

export interface BudgetEmissionPerPerson {
  meal: number;
  day: number;
}

export interface ComparisonResponse {
  comparisons: Comparison[];
  avg_emission_per_person: AvgEmissionPerPerson;
  budget_emission_per_person: BudgetEmissionPerPerson;
}
