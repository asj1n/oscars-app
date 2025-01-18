from flask import abort, render_template, Flask
import logging as log
import DataBaseConnection

APP = Flask(__name__)

@APP.route('/')
def index():
    stats = DataBaseConnection.execute('''
    SELECT * FROM (
      (SELECT COUNT(*) n_Ceremony FROM Ceremonies)
    JOIN
      (SELECT COUNT(*) n_Class FROM Categories)
    JOIN
      (SELECT COUNT(*) n_FilmId FROM Films)
    JOIN 
      (SELECT COUNT(*) n_NomId FROM Nominations)
    JOIN 
      (SELECT COUNT(*) n_UnNomineeId FROM Nominees)
    JOIN                                                                    
      (SELECT COUNT(*) n_Name FROM NomNames)
    JOIN 
      (SELECT COUNT(*) n_NomIdAux FROM NomNominees)
    );
    ''').fetchone()
    return render_template('index.html', stats = stats)


@APP.route("/diagram/")
def showDiagram():
    return render_template('diagram.html')


@APP.route('/ceremonies/')
def listCeremonies():
    ceremonies = DataBaseConnection.execute(
        '''
        SELECT Ceremony, Year
        FROM Ceremonies
        ORDER BY Ceremony
        ''').fetchall()
    return render_template('listCeremonies.html', ceremonies = ceremonies)


@APP.route('/categories/')
def listCategories():
    categories = DataBaseConnection.execute(
        '''
        SELECT Category, CanonicalCategory, Class
        FROM Categories
        ORDER BY Category
        ''').fetchall()
    return render_template('listCategories.html', categories = categories)


@APP.route('/films/')
def listFilms():
    films = DataBaseConnection.execute(
        '''
        SELECT FilmId, FilmName
        FROM Films
        ORDER BY FilmId
        ''').fetchall()
    return render_template('listFilms.html', films = films)
         

@APP.route('/nominations/')
def listNominations():
    nominations = DataBaseConnection.execute(
        '''
        SELECT NomId, Ceremony, Category, FilmId, Winner, Detail, Note, Citation, MultifilmNomination
        FROM Nominations
        ORDER BY Ceremony
        ''').fetchall()
    return render_template('listNominations.html', nominations = nominations)


@APP.route('/nominees/')
def listNominees():
    nominees = DataBaseConnection.execute(
        '''
        SELECT UnNomineeId, Nominee, NomineeIds
        FROM Nominees
        ''').fetchall()
    return render_template('listNominees.html', nominees = nominees)


@APP.route('/nomnames/')
def listNomNames():
    nomnames = DataBaseConnection.execute(
        '''
        SELECT NomId, Name
        FROM NomNames
        ''').fetchall()
    return render_template('listNomNames.html', nomnames = nomnames)


@APP.route('/nomnominees/')
def listNomNominees():
    nomnominees = DataBaseConnection.execute(
        '''
        SELECT UnNomineeId, NomId
        FROM NomNominees
        ''').fetchall()
    return render_template('listNomNominees.html', nomnominees = nomnominees)


@APP.route('/query1/')
def query1():
    query1 = DataBaseConnection.execute(
        '''
        SELECT Class, Category
        FROM Categories
        ORDER BY Class;  
        ''').fetchall()
    NumResults = len(query1)
    return render_template('query1.html', query1 = query1, NumResults = NumResults)


@APP.route('/query2/')
def query2():
    query2 = DataBaseConnection.execute(
        '''
        SELECT Class, COUNT(Category) AS NumCategorias
        FROM Categories
        GROUP BY Class
        ORDER BY NumCategorias DESC;
        ''').fetchall()
    NumResults = len(query2)
    return render_template('query2.html', query2 = query2, NumResults = NumResults)


@APP.route('/query3/<expr>/')
def query3_search(expr):
    search = { 'expr': expr }
    expr = '%' + expr + '%'
    query3_search = DataBaseConnection.execute(
        ''' 
        SELECT COUNT(*) AS NumOscars
        FROM Nominations n
            JOIN NomNames nn ON n.NomId = nn.NomId
        WHERE nn.name LIKE ? AND n.Winner = 'TRUE';
        ''', [expr]).fetchall()
    NumResults = len(query3_search)
    return render_template('query3_search.html', query3_search = query3_search, NumResults = NumResults)


@APP.route('/query4/')
def query4():
    query4 = DataBaseConnection.execute(
        '''
        SELECT DISTINCT c.Year, n.Category, nn.Name, n.Detail AS Role
        FROM Nominations n
                JOIN NomNames nn ON n.NomId = nn.NomId
                JOIN Ceremonies c ON c.Ceremony = n.Ceremony
                JOIN Categories cat ON cat.Category = n.Category
        WHERE cat.Class = 'Acting' AND n.Winner = 'TRUE';
        ''').fetchall()
    NumResults = len(query4)
    return render_template('query4.html', query4 = query4, NumResults = NumResults)


@APP.route('/query5/')
def query5():
    query5 = DataBaseConnection.execute(
        '''
        SELECT ni.Nominee, COUNT() OscarsWon
        FROM Nominations n 
            JOIN Categories c ON n.Category = c.Category
            JOIN NomNominees nn ON n.NomId = nn.NomId
            JOIN Nominees ni ON nn.UnNomineeId = ni.UnNomineeId
        WHERE c.Class = 'Acting' AND n.Winner = 'TRUE' AND ni.NomineeIds LIKE 'nm%'
        GROUP BY ni.NomineeIds
        HAVING OscarsWon >= 2
        ORDER BY OscarsWon DESC;
        ''').fetchall()
    NumResults = len(query5)
    return render_template('query5.html', query5 = query5, NumResults = NumResults)


@APP.route('/query6/')
def query6():
    query6 = DataBaseConnection.execute(
        '''
        SELECT ni.Nominee, COUNT() NumNominations
        FROM Nominations n 
            JOIN Categories c ON n.Category = c.Category
            JOIN NomNominees nn ON n.NomId = nn.NomId
            JOIN Nominees ni ON nn.UnNomineeId = ni.UnNomineeId
        WHERE c.Class = 'Acting' AND ni.NomineeIds LIKE 'nm%'
        GROUP BY ni.NomineeIds
        ORDER BY NumNominations DESC;
        ''').fetchall()
    NumResults = len(query6)
    return render_template('query6.html', query6 = query6, NumResults = NumResults)


@APP.route('/query7/')
def query7():
    query7 = DataBaseConnection.execute(
        '''
        SELECT c.Year, f.FilmName 
        FROM Nominations n 
            JOIN Ceremonies c ON n.Ceremony = c.Ceremony 
            JOIN Films f ON f.FilmId = n.FilmId 
            JOIN Categories cat ON cat.Category = n.Category 
        WHERE 1939 <= c.Year AND c.Year <= 1945 
            AND cat.CanonicalCategory = 'BEST PICTURE' 
            AND n.Winner = 'TRUE';
        ''').fetchall()
    NumResults = len(query7)
    return render_template('query7.html', query7 = query7, NumResults = NumResults)


@APP.route('/query8/')
def query8():
    query8 = DataBaseConnection.execute(
        '''
        SELECT c.Year, n.Category, COUNT() AS Num
        FROM Nominations n 
            JOIN NomNominees nn on n.NomId = nn.NomId
            JOIN Nominees ni on nn.UnNomineeId = ni.UnNomineeId
            JOIN Ceremonies c on c.Ceremony = n.Ceremony
        GROUP BY n.NomId
        HAVING Num >= 10
        ORDER BY c.Year;
        ''').fetchall()
    NumResults = len(query8)
    return render_template('query8.html', query8 = query8, NumResults = NumResults)


@APP.route('/query9/')
def query9():
    query9 = DataBaseConnection.execute(
        '''
        SELECT DISTINCT f.FilmId, f.FilmName
        FROM Nominations n
            JOIN Films f ON n.FilmId = f.FilmId
            JOIN Ceremonies c ON c.Ceremony = n.Ceremony
        WHERE n.FilmId NOT IN (
                    SELECT n.FilmId
                    FROM Nominations n 
                        JOIN Films f ON n.FilmId = f.FilmId
                    WHERE n.Winner != 'TRUE')
        ORDER BY c.Year;
        ''').fetchall()    
    NumResults = len(query9)
    return render_template('query9.html', query9 = query9, NumResults = NumResults)


@APP.route('/query10/')
def query10():
    query10 = DataBaseConnection.execute(
        '''
        SELECT f.FilmName, COUNT(*) AS NumOscars
        FROM Nominations n
            JOIN Films f ON f.FilmId =n.FilmId
        WHERE n.Winner IS 'TRUE'
        GROUP BY f.FilmId
        HAVING NumOscars = (
                SELECT MAX(Oscars)
                FROM (
                    SELECT COUNT() AS Oscars
                    FROM Nominations n
                            JOIN Films f ON f.FilmId = n.FilmId
                    WHERE n.Winner IS 'TRUE'
                    GROUP BY f.FilmId));
        ''').fetchall()    
    NumResults = len(query10)
    return render_template('query10.html', query10 = query10, NumResults = NumResults)


@APP.route('/query11/')
def query11():
    query11 = DataBaseConnection.execute(
        '''
        WITH aux AS
        (
        SELECT COUNT() numberWinners
        FROM
            (
            SELECT DISTINCT n.FilmId
            FROM Nominations n 
                JOIN Films f ON n.FilmId = f.FilmId
            WHERE n.Winner = 'TRUE'))
            
        SELECT ROUND((numberWinners*1.0/(SELECT COUNT() numberTotal FROM Films))*100,1) AS PercentageOfWinners
        FROM aux;
        ''').fetchall()
    NumResults = len(query11)
    return render_template('query11.html', query11 = query11, NumResults = NumResults)


@APP.route('/query12/')
def query12():
    query12 = DataBaseConnection.execute(
        '''
        SELECT nn.Name, count(n.Winner) AS NominatedAndLost
        FROM Nominations n
            JOIN NomNames nn ON n.NomId = nn.NomId
            JOIN Categories c ON c.Category = n.Category
        WHERE n.Winner NOT IN ('TRUE') AND c.Class = 'Acting'
        GROUP BY nn.Name
        HAVING (nn.Name, NominatedAndLost) IN (
                SELECT nn.Name, count(n.Winner) AS numTimesNominated
                FROM Nominations n
                    JOIN NomNames nn ON n.NomId = nn.NomId
                    JOIN Categories c ON c.Category = n.Category
                WHERE c.Class = 'Acting'
                GROUP BY nn.Name)
        AND NominatedAndLost >= 3
        ORDER BY NominatedAndLost DESC;
        ''').fetchall()
    NumResults = len(query12)
    return render_template('query12.html', query12 = query12, NumResults = NumResults)


@APP.route('/query13/')
def query13():
    query13 = DataBaseConnection.execute(
        '''
        SELECT c1.CanonicalCategory, ni1.Nominee, COUNT() AS Num
        FROM Nominations n1 
            JOIN Categories c1 ON n1.Category = c1.Category
            JOIN NomNominees nn1 ON n1.NomId = nn1.NomId
            JOIN Nominees ni1 ON nn1.UnNomineeId = ni1.UnNomineeId
        WHERE ni1.UnNomineeId = (
                SELECT ni2.UnNomineeId
                FROM Nominations n2 
                    JOIN Categories c2 ON n2.Category = c2.Category
                    JOIN NomNominees nn2 ON n2.NomId = nn2.NomId
                    JOIN Nominees ni2 ON nn2.UnNomineeId = ni2.UnNomineeId
                WHERE c2.CanonicalCategory = c1.CanonicalCategory
                GROUP BY ni2.Nominee
                ORDER BY COUNT(ni2.UnNomineeId) DESC
                LIMIT 1
                )
        GROUP BY c1.CanonicalCategory
        ORDER BY c1.CanonicalCategory;
        ''').fetchall()
    NumResults = len(query13)
    return render_template('query13.html', query13 = query13, NumResults = NumResults)