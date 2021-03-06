import transaction

from ..exceptions import BadIngredientInput, RecipeDoesntExist
from ..models import Recipe, RecipeIngredient, Ingredient


def delete_recipe(db, params):
    """
    Deletes a recipe by removing it from Recipe table and any reference from RecipeIngredient

    Args:
        db: database session
        params: (dict) must contain keys 'recipe_name', 'ingredients', and 'directions'
    """
    recipe_name = params.get('recipe_name').strip().lower()

    if not recipe_name:
        raise BadIngredientInput

    recipe = db.query(Recipe).filter_by(name=recipe_name).first()
    if not recipe:
        raise RecipeDoesntExist

    recipe_id = recipe.id

    ingredient_ids = {r.ingredient_id for r in db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()}
    with transaction.manager:
        db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).delete()
        db.delete(recipe)

    for ingredient_id in ingredient_ids:
        remaining_recipes = db.query(RecipeIngredient).filter(RecipeIngredient.ingredient_id == ingredient_id).count()
        if not remaining_recipes:  # Remove orphans
            with transaction.manager:
                db.query(Ingredient).filter(Ingredient.id == ingredient_id).delete()

    return True