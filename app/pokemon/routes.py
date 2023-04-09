from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .findpoke import findpokemon

from .forms import SearchPokemonForm, SearchUsersForm
from ..models import Pokemon, User

pokemon = Blueprint('pokemon', __name__, template_folder='poke_templates')

@pokemon.route('/pokemon/search', methods=['GET', 'POST'])
@login_required
def searchpokemon():
    form= SearchPokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.name.data.lower()
            poke = Pokemon.query.filter_by(name=pokemon_name).first()
            if poke:
                poke = poke.convertDict()
                return render_template('display_pokemon.html', p = poke)
            else:
                poke = findpokemon(pokemon_name)
                if poke:
                    pokemon = Pokemon(front_shiny=poke['Front Shiny'], name=poke['Name'], ability=poke['Ability'],
                                    base_hp=poke['Base HP'], base_atk=poke['Base ATK'], base_def=poke['Base DEF'])
                    pokemon.savePokemon()
                    # x=Pokemon.query.get(pokemon)
                    # print(x)
                    return render_template('display_pokemon.html', p = poke)
                else:
                    flash("This pokemon doesn't exist")
                    return redirect(url_for('pokemon.searchpokemon'))
        else:
            flash("This pokemon doesn't exist")
            return render_template('search_pokemon.html', form=form)
    return render_template('search_pokemon.html', form=form)

        # if pokemon is in database return pokemon
        # if pokemon is not in database, get it from
        # API and add to database for next time somebody searches
        # pokemon. return pokemon
@pokemon.route('/pokemon/users', methods=['GET', 'POST'])
@login_required
def users():
    #search for users
    form = SearchUsersForm()
    if request.method == 'POST':
        if form.validate():
            user_name = form.username.data.lower()
            user = User.query.filter_by(username=user_name).first()
            if user:
                return render_template('display_users.html', user=user)
            else:
                flash("User doesn't exist")
                return redirect(url_for('pokemon.users'))
    return render_template('search_users.html', form=form)
@pokemon.route('/pokemon/allusers')
@login_required
def allUsers():
    aUser=User.query.all()
    user_info = []
    for a in aUser:
        team=a.caught.all()
        user_info.append(team)
    print(user_info)
    return render_template('users.html', aUser=aUser)
    #displays all users and their teams
    #or i am display their team on a different html when clicked

@pokemon.route('/pokemon/viewteam/<int:user_id>')
@login_required
def viewTeam(user_id):
    user=User.query.get(user_id)
    users_pokemon = user.caught.all()
    print(users_pokemon)
    return render_template('view_team.html', team=users_pokemon)

@pokemon.get('/pokemon/catch/<name>')
@login_required
def catch(name):
    poke_name = Pokemon.query.filter_by(name=name).first()
    print(poke_name)
    if not poke_name.isCaught:
        current_user_poke_count = len(current_user.caught.all())
        if current_user_poke_count >=5:
            flash('Your team is full!')
            return redirect(url_for('pokemon.team'))
        else:
            poke_name.gotCaught()
            current_user.catch_poke(poke_name)
            return redirect(url_for('pokemon.team'))
    flash('This pokemon is already caught!')
    return redirect(url_for('pokemon.searchpokemon'))
@pokemon.get('/pokemon/release/<name>')
@login_required
def releaseFunc(name):
    # poke_name = catch.get(user_id)
    # c = Pokemon.query.filter_by(name=name).first()
    # if c.caught:
    #     if current_user.name == poke_name.name:
    #         poke_name.gotCaught()
    #         current_user.release(poke_name)
    #         return render_template('team.html', p=poke_name.convertDict())
    # return redirect(url_for('team.html'))
    poke_name = Pokemon.query.filter_by(name=name).first()
    if poke_name.isCaught:
        # if current_user.id == poke_name.caught_by:
        poke_name.gotCaught()
        current_user.release(poke_name)
        return redirect(url_for('pokemon.team'))
    flash("You haven't caught this Pokemon!")
    return redirect(url_for('pokemon.team'))

@pokemon.route('/pokemon/team')
@login_required
def team():
    #if the current_user.name is equal to the name in catch table
    #render pokemon
    team = current_user.caught.all()
    print(team)
    return render_template('team.html', team=team)

@pokemon.route('/pokemon/battle/<int:user_id>')
@login_required
def battle(user_id):
    enemy = User.query.get(user_id)
    my_team = current_user.caught.all()
    enemy_team = enemy.caught.all()
    my_stats = 0
    enemy_stats = 0
    for m in my_team:
        hp = (m.base_hp)
        attack = (m.base_atk)
        defense = (m.base_def)
        my_total = hp + attack + defense
        my_stats+= my_total
    for e in enemy_team:
        hp = (e.base_hp)
        attack = (e.base_atk)
        defense = (e.base_def)
        enemy_total = hp + attack + defense
        enemy_stats += enemy_total
    if my_stats >= enemy_stats:
        current_user.win()
        enemy.lose()
        return render_template('winner.html')
    else:
        current_user.lose()
        enemy.win()
        return render_template('loser.html')
    
