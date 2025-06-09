export interface IngredientOutput {
  name: string;
  ingredient_id?: string | null;
  weight_kg?: number | null;
  co2_per_kg?: number | null;
  co2_kg?: number | null;
  calculation_notes?: string | null;
  weight_estimation_notes?: string | null;
  co2_emission_notes?: string | null;
}

export interface RecipeCO2Output {
  title?: string | null;
  url: string;
  total_co2_kg: number;
  number_of_persons?: number | null;
  co2_per_person_kg?: number | null;
  avg_meal_emission_per_person_range_kg: number[];
  ingredients: IngredientOutput[];
}

export interface ComparisonResponse {
  input_co2_kg: number;
  reference_kg: number;
  ratio: number;
  helperText: string;
}
