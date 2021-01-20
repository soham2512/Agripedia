from flask import render_template

from project import app


@app.route('/user/criticalFactors', methods=['GET', 'POST'])
def userLoadCriticalFactors():
    try:
        return render_template('user/CriticalFactors.html')
    except Exception as ex:
        print(ex)


@app.route('/user/tipsForFarmers', methods=['GET', 'POST'])
def userLoadTipsForFarmers():
    try:
        return render_template('user/TipsForFarmers.html')
    except Exception as ex:
        print(ex)


@app.route('/user/organicFarming', methods=['GET', 'POST'])
def userLoadOrganicFarming():
    try:
        return render_template('user/OrganicFarming.html')
    except Exception as ex:
        print(ex)


@app.route('/user/ImportantPortals', methods=['GET', 'POST'])
def userLoadImportantPortals():
    try:
        return render_template('user/ImportantPortals.html')
    except Exception as ex:
        print(ex)


@app.route('/user/AdvanceTechnologies', methods=['GET', 'POST'])
def userLoadAdvanceTechnologies():
    try:
        return render_template('user/AdvanceTechnologies.html')
    except Exception as ex:
        print(ex)


@app.route('/user/WeatherInformation', methods=['GET', 'POST'])
def userLoadWeatherInformation():
    try:
        return render_template('user/WeatherInformation.html')
    except Exception as ex:
        print(ex)
