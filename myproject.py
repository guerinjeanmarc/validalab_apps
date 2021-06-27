#!/usr/bin/env python
import os
from json import dumps
from flask import Flask, g, Response, request, jsonify

from neo4j import GraphDatabase, basic_auth

app = Flask(__name__, static_url_path='/static/')

password = os.getenv("NEO4J_PASSWORD")
password = "dfg"
ip = "163.172.110.238"

driver = GraphDatabase.driver('bolt://'+ip,auth=basic_auth("neo4j", password))
#rajouter la base prod

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session(database='jmdemo')
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

@app.route("/")
def get_index():
    return app.send_static_file('index_medias_copie.html')
@app.route("/twit")
def get_index_1():
    return app.send_static_file('index_medias_twit.html')
@app.route("/yout")
def get_index_2():
    return app.send_static_file('index_medias_yout.html')
@app.route("/ent")
def get_index_3():
    return app.send_static_file('index_medias_ent.html')

@app.route("/custom")
def get_index_4():
    return app.send_static_file('index_medias_entities.html')

@app.route("/custom_test")
def get_index_5():
    return app.send_static_file('index_test.html')



def serialize_web_details(record):
    ACPM_stats =""
    if record['w']["ACPM_SiteGP_Rang"] != None:
        visites = str(record['w']["ACPM_SiteGP_Visites totales"])
        pages = str(record['w']["ACPM_SiteGP_Pages Vues Totales"])
        rang = str(record['w']["ACPM_SiteGP_Rang"])
        gp = " (grand public)"
        ACPM_stats = "ACPM stats mensuelles : " + visites + " visites, " + pages + " pages vues, rang : " + rang + gp
    if record['w']["ACPM_SitePro_Rang"] != None:
        visites = str(record['w']["ACPM_SitePro_Visites totales"])
        pages = str(record['w']["ACPM_SitePro_Pages Vues Totales"])
        rang = str(record['w']["ACPM_SitePro_Rang"])
        gp = " (professionnel)"
        ACPM_stats = "ACPM stats mensuelles : " + visites + " visites, " + pages + " pages vues, rang : " + rang + gp

    diplo = None
    if record['e']['Diplo_typeCode']==1:
        if record['e']['Diplo_rangChallenges'] != None:
            diplo = "Personne physique " + str(record['e']['Diplo_rangChallenges']) + "/500 plus riches de France (challenges)"
        else:
            diplo = "Personne physique "
    if record['e']['Diplo_typeCode']==2:
        diplo = "Personne morale"
    if record['e']['Diplo_typeCode']==3:
        diplo = "Média : "+ str(record['e']['Diplo_mediaType']) + " "+ str(record['e']['Diplo_mediaPeriodicite']) +" "+ str(record['e']['Diplo_mediaEchelle'])+" "+ str(record['e']['Diplo_commentaire'])

    DAT = None
    if record['w']['DAT_SitesLabellisés'] != None:
        DAT = "DigitalAdTrust : " + str(record['w']['DAT_SitesLabellisés']) + " | " + str(record['w']['DAT_Périmètresdulabel'])
    try:
        d_stat1 = str(record['w']['D2_pages_total'][0]) +" pages trouvées, cité par "+ str(record['w']['D2_indegree'][0]) +" sites"
    except:
        d_stat1=None

    try:
        e_wikisummary = str(record['wiki']['summary']) + " (wikipedia)"
    except:
        e_wikisummary=None

    return {
        'd_title': record['wtype'],
        'd_sitename': record['w']['name'],
        'd_name': record['w']['name'],
        'd_stat1': d_stat1,
        'd_stat2': ACPM_stats,
        'd_DAT': DAT,

        'site_name': record['name'],
        'type': record['type'],
        'cite': record['cite'],
        'estcite': record['estcite'],

        'entity_name':record['e']['name'],
        'e_diplo': diplo,
        'e_wikisummary': e_wikisummary,
        'e_Spiil': "SPIIL : "+ str(record['w']['SPIIL_Nomducompte']) + " | " + str(record['w']['SPIIL_Formejuridique']) + " | " + str(record['w']['SPIIL_Région']),
        'e_CPPAP': "CPPAP : " + str(record['w']['CPPAP_Editeur']) + " | " + str(record['w']['CPPAP_FormeJuridique']) + " | " + str(record['w']['CPPAP_Qualification']),
        'e_ML': "Media_locaux : " + str(record['w']['ML_communes']) + " | " + str(record['w']['ML_site_name']) + " | " + str(record['w']['ML_medias']) + " | " + str(record['w']['ML_typesmedia'])
    }

def serialize_twit_details(record):
    verified = " : "
    if record['w']['verified']:
        verified = " compte vérifié : "

    try:
        cite = str(record['t2']['friends_count']) +" abonnements"
        estcite = str(record['t2']['followers_count']) +" abonnés"
    except:
        cite=None
        estcite=None

    try:
        e_wikisummary = str(record['wiki']['summary']) + " (wikipedia)"
    except:
        e_wikisummary=None

    try:
        e_Spiil = "SPIIL : "+ str(record['w']['SPIIL_Nomducompte']) + " | " + str(record['w']['SPIIL_Formejuridique']) + " | " + str(record['w']['SPIIL_Région'])
        e_CPPAP = "CPPAP : " + str(record['w']['CPPAP_Editeur']) + " | " + str(record['w']['CPPAP_FormeJuridique']) + " | " + str(record['w']['CPPAP_Qualification'])
        e_ML = "Media_locaux : " + str(record['w']['ML_communes']) + " | " + str(record['w']['ML_site_name']) + " | " + str(record['w']['ML_medias']) + " | " + str(record['w']['ML_typesmedia'])
    except:
        e_Spiil = None
        e_CPPAP = None
        e_ML = None

    diplo = None
    if record['e']['Diplo_typeCode']==1:
        if record['e']['Diplo_rangChallenges'] != None:
            diplo = "Personne physique " + str(record['e']['Diplo_rangChallenges']) + "/500 plus riches de France (challenges)"
        else:
            diplo = "Personne physique "
    if record['e']['Diplo_typeCode']==2:
        diplo = "Personne morale"
    if record['e']['Diplo_typeCode']==3:
        diplo = "Média : "+ str(record['e']['Diplo_mediaType']) + " "+ str(record['e']['Diplo_mediaPeriodicite']) +" "+ str(record['e']['Diplo_mediaEchelle'])+" "+ str(record['e']['Diplo_commentaire'])


    return {
        'd_title': record['wtype'],
        'd_sitename': record['t']['name'],
        'd_name': str(record['t']['name']) + verified + str(record['t']['description']),
        'd_loc': "localisation : " + str(record['t']['location']) + " | créé le " + str(record['t']['created_at']),
        'd_stat1': str(record['t']['statuses_count']) + " tweets, "+ str(record['t']['friends_count']) +" abonnements, " + str(record['t']['followers_count']) +" abonnés",
        'd_stat2': "",

        'site_name': record['name'],
        'type': record['type'],
        'cite': cite,
        'estcite': estcite,


        'entity_name':record['e']['name'],
        'e_diplo': diplo,
        'e_wikisummary': e_wikisummary,
        'e_Spiil': e_Spiil,
        'e_CPPAP': e_CPPAP,
        'e_ML': e_ML
    }

def serialize_youtube_details(record):
    try:
        e_wikisummary = str(record['wiki']['summary']) + " (wikipedia)"
    except:
        e_wikisummary = None

    try:
        e_Spiil = "SPIIL : "+ str(record['w']['SPIIL_Nomducompte']) + " | " + str(record['w']['SPIIL_Formejuridique']) + " | " + str(record['w']['SPIIL_Région'])
        e_CPPAP = "CPPAP : " + str(record['w']['CPPAP_Editeur']) + " | " + str(record['w']['CPPAP_FormeJuridique']) + " | " + str(record['w']['CPPAP_Qualification'])
        e_ML = "Media_locaux : " + str(record['w']['ML_communes']) + " | " + str(record['w']['ML_site_name']) + " | " + str(record['w']['ML_medias']) + " | " + str(record['w']['ML_typesmedia'])
    except:
        e_Spiil = None
        e_CPPAP = None
        e_ML = None

    diplo = None
    if record['e']['Diplo_typeCode']==1:
        if record['e']['Diplo_rangChallenges'] != None:
            diplo = "Personne physique " + str(record['e']['Diplo_rangChallenges']) + "/500 plus riches de France (challenges)"
        else:
            diplo = "Personne physique "
    if record['e']['Diplo_typeCode']==2:
        diplo = "Personne morale"
    if record['e']['Diplo_typeCode']==3:
        diplo = "Média : "+ str(record['e']['Diplo_mediaType']) + " "+ str(record['e']['Diplo_mediaPeriodicite']) +" "+ str(record['e']['Diplo_mediaEchelle'])+" "+ str(record['e']['Diplo_commentaire'])


    return {
        'd_title': record['wtype'],
        'd_sitename': record['t']['name'],
        'd_name': str(record['t']['pro_title']) + " : " + str(record['t']['pro_description']),
        'd_loc': "localisation : " + str(record['t']['pro_country']) + " | créé le " + str(record['t']['pro_publishedAt']),
        'd_stat1': str(record['t']['pro_videoCount']) + " videos, "+ str(record['t']['pro_subscriberCount']) +" abonnés, " + str(record['t']['pro_viewCount']) +" vues",
        'd_stat2': "",

        'site_name': record['name'],
        'type': record['type'],
        'cite': str(record['t2']['pro_subscriberCount']) +" abonnés",
        'estcite': str(record['t2']['pro_subscriberCount']) +" vues",


        'entity_name':record['e']['name'],
        'e_diplo': diplo,
        'e_wikisummary': e_wikisummary,
        'e_Spiil': e_Spiil,
        'e_CPPAP': e_CPPAP,
        'e_ML': e_ML
        }

def serialize_search(record):
    return{
        'site_name': record['name'],
        'type': record['type'],
        'entity': record['e.name']
    }

@app.route("/twit_graph")
def get_twit_graph():
    db = get_db()
    # debug
    # db = driver.session()
    sizeProp = 'PageRank'
    colorProp = 'LouvainCommunity'
    reltype = 'LINKS_TO_tot'

    results = db.run(
        "MATCH path=(w1:Twitter)-[]->(w2:Twitter)-[]->(w1)"
        "RETURN w1.name as W1, w1.PageRanktot as w1pr, "
        "w2.name as W2, w2.PageRanktot as w2pr "
        )

    nodes=[]
    rels=[]
    for record in results:

        # Replaced this 2 lines by the others
        w1 = {"name": record["W1"], "label": "Twitter", "size": record["w1pr"]*10, "Community": 1 }
        w2 = {"name": record["W2"], "label": "Twitter", "size": record["w2pr"]*10, "Community": 1}

        try:
            w1_id = nodes.index(w1)
        except:
            nodes.append(w1)
            w1_id = nodes.index(w1)
        try:
            w2_id = nodes.index(w2)
        except:
            nodes.append(w2)
            w2_id = nodes.index(w2)

        #count = record["W1W2count"] +record["W2W1count"]
        rel = {'source': w1_id, 'target': w2_id, 'count': 0}
        if rel not in rels:
            rels.append(rel)

    for node in nodes:
        node['id']=nodes.index(node)
        print(node)

    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

@app.route("/web_graph")
def get_web_graph():
    db = get_db()

    # debug
    # db = driver.session()

    sizeProp = 'PageRank'
    colorProp = 'LouvainCommunity'
    reltype = 'LINKS_TO_tot'

    results = db.run(
        "MATCH path=(w1:Website {WCC_bij:945})-[:LINKS_TO_tot_bij]-(w2:Website)"
        "RETURN w1.site_name as W1, w1.PageRank as w1pr, w1.fiability as w1c,"
        "w2.site_name as W2, w2.PageRank as w2pr, w2.fiability as w2c"
         ,{"sizeProp": sizeProp}
        )

    nodes=[]
    rels=[]
    for record in results:
        # Replaced this 2 lines by the others
        w1 = {"name": record["W1"], "label": "website", "size": record["w1pr"]*10, "Community": record["w1c"] }
        w2 = {"name": record["W2"], "label": "website", "size": record["w2pr"]*10, "Community": record["w2c"]}
        #w1 = {"name": record["W1"], "label": "website", "size": record["w1pr"]*10, "Community": record["w1c"],"entitiy_name":record['entity_name1'] }
        #w2 = {"name": record["W2"], "label": "website", "size": record["w2pr"]*10, "Community": record["w2c"],"entitiy_name":record['entity_name2']}
        #w1 = {"name": record["W1"], "label": "website", "size": 5, "Community": 1}
        #w2 = {"name": record["W2"], "label": "website", "size": 5, "Community": 1}

        try:
            w1_id = nodes.index(w1)
        except:
            nodes.append(w1)
            w1_id = nodes.index(w1)
        try:
            w2_id = nodes.index(w2)
        except:
            nodes.append(w2)
            w2_id = nodes.index(w2)

        rel = {'source': w1_id, 'target': w2_id, 'count': 0}
        if rel not in rels:
            rels.append(rel)

    for node in nodes:
        node['id']=nodes.index(node)
        print(node)

    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

@app.route("/yout_graph")
def get_yout_graph():
    db = get_db()
    # debug
    # db = driver.session()

    results = db.run(
        "MATCH path=(w1:Youtube)-[]->(w2:Youtube)"
        "RETURN w1.name as W1, w1.PageRanktot as w1pr, "
        "w2.name as W2, w2.PageRanktot as w2pr "
        )

    nodes=[]
    rels=[]
    for record in results:

        # Replaced this 2 lines by the others
        w1 = {"name": record["W1"], "label": "Youtube", "size": record["w1pr"]*10, "Community": 1 }
        w2 = {"name": record["W2"], "label": "Youtube", "size": record["w2pr"]*10, "Community": 1}

        try:
            w1_id = nodes.index(w1)
        except:
            nodes.append(w1)
            w1_id = nodes.index(w1)
        try:
            w2_id = nodes.index(w2)
        except:
            nodes.append(w2)
            w2_id = nodes.index(w2)

        #count = record["W1W2count"] +record["W2W1count"]
        rel = {'source': w1_id, 'target': w2_id, 'count': 0}
        if rel not in rels:
            rels.append(rel)

    for node in nodes:
        node['id']=nodes.index(node)
        print(node)

    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

@app.route("/ent_graph")
def get_ent_graph():
    db = get_db()

    # debug
    # db = driver.session()

    sizeProp = 'PageRank'
    colorProp = 'LouvainCommunity'
    reltype = 'LINKS_TO_tot'

    results = db.run(
        "MATCH path=(e1:Entity)-[]-(w1:Website)-[:LINKS_TO_tot_bij]-(w2:Website)-[]-(e2:Entity) "
        "RETURN e1.name as W1, e1.PageRanktot as w1pr, e2.name as W2, e2.PageRanktot as w2pr "
        "UNION "
        "MATCH path=(e3:Entity)-[]-(w3:Twitter)-[:FOLLOWS_bij]-(w4:Twitter)-[]-(e4:Entity) "
        "RETURN e3.name as W1, e3.PageRanktot as w1pr, e4.name as W2, e4.PageRanktot as w2pr "
        )

    nodes=[]
    rels=[]
    for record in results:
        # Replaced this 2 lines by the others
        w1 = {"name": record["W1"], "label": "website", "size": record["w1pr"]*10, "Community": 1 }
        w2 = {"name": record["W2"], "label": "website", "size": record["w2pr"]*10, "Community": 1 }

        #w1 = {"name": record["W1"], "label": "website", "size": 5, "Community": 1}
        #w2 = {"name": record["W2"], "label": "website", "size": 5, "Community": 1}

        try:
            w1_id = nodes.index(w1)
        except:
            nodes.append(w1)
            w1_id = nodes.index(w1)
        try:
            w2_id = nodes.index(w2)
        except:
            nodes.append(w2)
            w2_id = nodes.index(w2)

        rel = {'source': w1_id, 'target': w2_id, 'count': 0}
        if rel not in rels:
            rels.append(rel)

    for node in nodes:
        node['id']=nodes.index(node)
        print(node)

    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        db = get_db()
        """ results = db.run("MATCH (w:Website) "
            "WHERE w.name =~ $site_name "
            "OPTIONAL MATCH (w)-[:OWNED_BY]->(e:Entity) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(n) "
            "WITH e, n, reduce(sum = 0, x IN collect(e.name)|sum + coalesce(n.PageRanktot,0)) AS sum "
            "RETURN n.name as name,LABELS(n)[0] as type, n.PageRanktot, e.name,sum order by e.name, sum desc",
            {"site_name": "(?i).*" + q + ".*"}) """
        """     results = db.run("MATCH (w:Website)-[:OWNED_BY]->(e:Entity) "
            "WHERE w.name =~ $site_name "
            "RETURN w.name as name,LABELS(w)[0] as type, w.PageRank, e.name order by w.PageRank desc",
            {"site_name": "(?i).*" + q + ".*"}) """



        results = db.run("MATCH (w:Website)-[:OWNED_BY]->(e:Entity) "
            "WHERE w.name =~ $site_name "
            "WITH COLLECT({name:w.name, type: LABELS(w)[0], pr: w.PageRank, ename: e.name}) as rows "
            "MATCH (w)<-[:RECOMMENDS]-() "
            "WHERE w.name =~ $site_name "
            "OPTIONAL MATCH (w)-[:OWNED_BY]->(e:Entity) "
            "with rows + COLLECT({name:w.name, type: LABELS(w)[0], pr: w.PageRank, ename: e.name}) as allRows "
            "UNWIND allRows as row "
            "with row.name as name, row.type as type, row.ename as ename, row.pr as pr "
            "RETURN DISTINCT name, type, pr, ename order by pr desc "
            ,{"site_name": "(?i).*" + q + ".*"})

        return Response(dumps([serialize_search(record) for record in results]),
            mimetype="application/json")
        #return Response(dumps([serialize_media(record[0]) for record in results]),
        #                mimetype="application/json")


@app.route("/media/<site_name>")
def get_media(site_name):
    typeList = ["Website", "Twitter", "Youtube", "Wikipedia", "Entity", "Linkedin"]
    nodename =  ""
    nodetype = ""
    entityname = ""
    for x in typeList:
        if len(site_name.split(x))>1:
            nodename =  site_name.split(x)[0]
            nodetype = x
            entityname = site_name.split(x)[1]

    db = get_db()
    resp=""
    if nodetype=="Website":
        results = db.run("MATCH (e:Entity )<-[:OWNED_BY]-(w:Website {name:$site_name})<-[r:LINKS_TO_tot]-(w2) "
            "OPTIONAL MATCH (w2)<-[r2:LINKS_TO_tot]-(w) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(wiki:Wikipedia) "
            "RETURN e, wiki ,w, LABELS(w)[0] as wtype , "
                " w2.name as name, LABELS(w2)[0] as type, sum(r.count) as cite, "
                "sum(r2.count) as estcite ORDER BY cite DESC LIMIT 3",
            {"site_name": nodename, "ent_name":entityname})
        resp = dumps([serialize_web_details(record) for record in results])

    if nodetype=="Twitter":
        results = db.run("MATCH (e:Entity )<-[:OWNED_BY]-(t:Twitter {name:$site_name})<-[r:FOLLOWS]-(t2) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(w:Website) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(wiki:Wikipedia) "
            "RETURN e, wiki ,t, LABELS(t)[0] as wtype , t2, w, "
                " t2.name as name, LABELS(t2)[0] as type, t2.PageRanktot as prtot "
                " ORDER BY prtot DESC LIMIT 3",
            {"site_name": nodename, "ent_name":entityname})
        resp = dumps([serialize_twit_details(record) for record in results])

    if nodetype=="Youtube":
        results = db.run("MATCH (e:Entity {name:$ent_name})<-[:OWNED_BY]-(t:Youtube {name:$site_name})<-[r:RECOMMENDS]-(t2) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(w:Website) "
            "OPTIONAL MATCH (e)<-[:OWNED_BY]-(wiki:Wikipedia) "
            "RETURN e, wiki ,t, LABELS(t)[0] as wtype , t2, w, "
                " t2.name as name, LABELS(t2)[0] as type, t2.PageRanktot as prtot "
                " ORDER BY prtot DESC LIMIT 3",
            {"site_name": nodename, "ent_name":entityname})
        resp = dumps([serialize_youtube_details(record) for record in results])

    return Response(resp, mimetype="application/json")

    #if nodetype=="Entity":
    #    results = db.run("MATCH (e:Entity {name:$ent_name})<-[:OWNED_BY]-(t:Entity {name:$site_name}) "
    #        "OPTIONAL MATCH (e)<-[:OWNED_BY]-(wiki1:Wikipedia) "
    #        "OPTIONAL MATCH (t)<-[:OWNED_BY]-(wiki2:Wikipedia) "
    #        "RETURN e, wiki ,t, LABELS(t)[0] as wtype , t2, w, "
    #            " t2.name as name, LABELS(t2)[0] as type, t2.PageRanktot as prtot "
    #            " ORDER BY prtot DESC LIMIT 3",
    #        {"site_name": nodename, "ent_name":entityname})
    #    resp = dumps([serialize_youtube_details(record) for record in results])

@app.route("/med/<site_name>", methods = ['GET'])
def get_media_1(site_name):
    
    db = get_db()
    results = db.run("match (n {name:$site_name})-[:OWNED_BY]->(r:Entity)<-[:OWNED_BY]-(w:Wikipedia) return w.summary",
                    {"site_name": site_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data())[0])
@app.route("/med_1/<ent_name>", methods = ['GET'])
def get_media_2(ent_name):
    
    db = get_db()
    results = db.run("match (w:Website {name:$ent_name})-[r:OWNED_BY*]->(e)<-[:OWNED_BY*]-(e2:Entity) return e2.name",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_2/<ent_name>", methods = ['GET'])
def get_media_3(ent_name):
    
    db = get_db()
    results = db.run("match (w:Website {name:$ent_name})-[r:OWNED_BY*]->(e) return e.name",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_3/<ent_name>", methods = ['GET'])
def get_media_4(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})-[:OWNED_BY]->(e:Entity)<-[:OWNED_BY]-(wiki:Wikipedia) return wiki.genre,wiki.categories[0]",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_4/<ent_name>", methods = ['GET'])
def get_media_5(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})return w.ACPM_SiteGP_Rang as gR,w.`ACPM_SiteGP_Visites totales` as gV, w.ACPM_SitePro_Rang as pR,w.`ACPM_SitePro_Visites totales` as pV",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_5/<ent_name>", methods = ['GET'])
def get_media_6(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})-[:OWNED_BY]->(e:Entity)<-[:OWNED_BY]-(tw:Twitter) return tw.user_name,tw.followers_count",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_6/<ent_name>", methods = ['GET'])
def get_media_7(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})-[:OWNED_BY]->(e:Entity)<-[:OWNED_BY]-(yt:Youtube) return yt.user_name,yt.pro_subscriberCount,yt.url",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_7/<ent_name>", methods = ['GET'])
def get_media_8(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})-[:OWNED_BY]->(e:Entity)<-[:OWNED_BY]-(fb:Facebook) return fb.user_name",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
@app.route("/med_8/<ent_name>", methods = ['GET'])
def get_media_9(ent_name):
    
    db = get_db()
    results = db.run("match(w:Website{name:$ent_name})-[r:LINKS_TO_tot_bij]->(w2) return w2.name, w2.PageRanktot ORDER BY w2.PageRanktot desc ",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))
    
@app.route("/med_9/<ent_name>", methods = ['GET'])
def get_media_10(ent_name):
    
    db = get_db()
    results = db.run("MATCH(w:Website{name:$ent_name})<-[reco:RECOMMENDS]-(r) RETURN r.name as recommender, reco.weight as weight, reco.meaning as meaning, reco.sourceURL as sourceURL;",
                    {"ent_name": ent_name})
            # {"site_name": nodename, "ent_name":entityname})
    return jsonify((results.data()))

"match(n:Website{name:'lemonde.fr'})-[:OWNED_BY*]->(e) where not (e)-[:OWNED_BY]->() return e.name"



if __name__ == '__main__':
    app.run(debug=True)


# %% sandbox
site_name = "lemonde.frWebsiteLe Monde"
typeList = ["Website", "Twitter", "Youtube", "Wikipedia", "Entity"]
#for x in typeList:
#    if len(site_name.split(x))>1:
#        print(x,site_name.split(x)[0],site_name.split(x)[1] )


#q
#results = db.run("MATCH (w) "
#         "WHERE w.site_name =~ $site_name "
#         "RETURN w LIMIT 10", {"site_name": "(?i).*" + q + ".*"}
#)
#dumps([serialize_media(record[0]) for record in results])


#results = db.run("MATCH (w) "
#    "WHERE w.name =~ $site_name "
#    "OPTIONAL MATCH (w)-[:OWNED_BY]->(e:Entity) "
#    "OPTIONAL MATCH (e)<-[:OWNED_BY]-(n) "
#    "WITH e, n, reduce(sum = 0, x IN collect(e.name)|sum + coalesce(n.PageRanktot,0)) AS sum "
#    "RETURN n.name as name,LABELS(n)[0] as type, n.PageRanktot, e.name,sum order by e.name, sum desc",
#    {"site_name": "(?i).*" + q + ".*"})
#dumps([serialize_search(record) for record in results])