from flask import render_template

from project import app


@app.route('/', methods=['GET', 'POST'])
def publicLoadDashboard():
    try:
        return render_template('public/index.html')
    except Exception as ex:
        print(ex)


@app.route('/public/criticalFactors', methods=['GET', 'POST'])
def publicLoadCriticalFactors():
    try:
        return render_template('public/CriticalFactors.html')
    except Exception as ex:
        print(ex)


@app.route('/public/tipsForFarmers', methods=['GET', 'POST'])
def publicLoadTipsForFarmers():
    try:
        return render_template('public/TipsForFarmers.html')
    except Exception as ex:
        print(ex)


@app.route('/public/organicFarming', methods=['GET', 'POST'])
def publicLoadOrganicFarming():
    try:
        return render_template('public/OrganicFarming.html')
    except Exception as ex:
        print(ex)


@app.route('/public/ImportantPortals', methods=['GET', 'POST'])
def publicLoadImportantPortals():
    try:
        return render_template('public/ImportantPortals.html')
    except Exception as ex:
        print(ex)


@app.route('/public/AdvanceTechnologies', methods=['GET', 'POST'])
def publicLoadAdvanceTechnologies():
    try:
        return render_template('public/AdvanceTechnologies.html')
    except Exception as ex:
        print(ex)


@app.route('/public/WeatherInformation', methods=['GET', 'POST'])
def publicLoadWeatherInformation():
    try:
        return render_template('public/WeatherInformation.html')
    except Exception as ex:
        print(ex)


@app.route('/public/AboutPdms', methods=['GET', 'POST'])
def publicLoadAboutPdms():
    try:
        return render_template('public/AboutPdms.html')
    except Exception as ex:
        print(ex)
