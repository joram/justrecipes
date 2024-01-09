#!/usr/bin/env python3
import asyncio
import json
import os

from bs4 import BeautifulSoup

from .caching import get_cached
from .get_schema_data import get_schema_data

# Roughly 300 websites
recipe_websites = [
    "https://claudia.abril.com.br/",
    "https://abuelascounter.com/",
    "https://www.acouplecooks.com",
    "https://addapinch.com/",
    "http://www.afghankitchenrecipes.com/",
    "https://akispetretzikis.com/",
    "https://ah.nl/",
    "https://allrecipes.com/",
    "https://alltommat.se/",
    "https://altonbrown.com/",
    "https://amazingribs.com/",
    "https://ambitiouskitchen.com/",
    "https://archanaskitchen.com/",
    "https://www.arla.se/",
    "https://www.atelierdeschefs.fr/",
    "https://averiecooks.com/",
    "https://barefootcontessa.com/",
    "https://baking-sense.com/",
    "https://bakingmischief.com/",
    "https://bbc.com/",
    "https://bbc.co.uk/",
    "https://bbcgoodfood.com/",
    "https://bettybossi.ch/",
    "https://bettycrocker.com/",
    "https://biancazapatka.com/",
    "https://bigoven.com/",
    "https://blueapron.com/",
    "https://bluejeanchef.com/",
    "https://bonappetit.com/",
    "https://www.bodybuilding.com/",
    "https://bongeats.com/",
    "https://bowlofdelicious.com/",
    "https://briceletbaklava.ch/",
    "https://budgetbytes.com/",
    "https://carlsbadcravings.com/",
    "https://castironketo.net/",
    "https://cdkitchen.com/",
    "https://chefkoch.de/",
    "https://www.chefnini.com/",
    "https://chefsavvy.com/",
    "https://closetcooking.com/",
    "https://comidinhasdochef.com/",
    "https://cookeatshare.com/",
    "https://cookieandkate.com/",
    "https://cookingcircle.com/",
    "https://cookinglight.com/",
    "https://cookpad.com/",
    "https://cookstr.com/",
    "https://cook-talk.com/",
    "https://www.coop.se/",
    "https://copykat.com/",
    "https://www.costco.com/",
    "https://countryliving.com/",
    "https://creativecanning.com/",
    "https://cucchiaio.it/",
    "https://cuisineaz.com/",
    "https://cybercook.com.br/",
    "https://www.davidlebovitz.com/",
    "https://delish.com/",
    "https://domesticate-me.com/",
    "https://downshiftology.com/",
    "https://www.dr.dk/",
    "https://www.eatingbirdfood.com/",
    "https://www.eatingwell.com/",
    "https://www.eatliverun.com/",
    "https://eatsmarter.com/",
    "https://eatsmarter.de/",
    "https://www.eatwell101.com",
    "https://eatwhattonight.com/",
    "https://elavegan.com/",
    "https://emmikochteinfach.de/",
    "https://ethanchlebowski.com/",
    "https://epicurious.com/",
    "https://www.errenskitchen.com/",
    "https://recipes.farmhousedelivery.com/",
    "https://www.farmhouseonboone.com/",
    "https://www.fattoincasadabenedetta.it/",
    "https://fifteenspatulas.com/",
    "https://finedininglovers.com/",
    "https://fitmencook.com/",
    "https://fitslowcookerqueen.com",
    "https://food.com/",
    "https://food52.com/",
    "https://foodandwine.com/",
    "https://foodnetwork.com/",
    "https://foodrepublic.com/",
    "https://www.forksoverknives.com/",
    "https://forktospoon.com/",
    "https://fredriksfika.allas.se/",
    "https://www.750g.com",
    "https://www.gesund-aktiv.com/",
    "https://giallozafferano.it/",
    "https://gimmesomeoven.com/",
    "https://godt.no/",
    "https://goodfooddiscoveries.com/",
    "https://goodhousekeeping.com/",
    "https://recietas.globo.com/",
    "https://gonnawantseconds.com/",
    "https://gousto.co.uk/",
    "https://www.grandfrais.com/",
    "https://greatbritishchefs.com/",
    "https://grimgrains.com/",
    "http://www.grouprecipes.com/",
    "https://halfbakedharvest.com/",
    "https://handletheheat.com/",
    "https://www.hassanchef.com/",
    "https://headbangerskitchen.com/",
    "https://heatherchristo.com/",
    "https://www.heb.com/",
    "https://hellofresh.com/",
    "https://hellofresh.co.uk/",
    "https://www.hellofresh.de/",
    "https://www.hellofresh.fr/",
    "https://www.hellofresh.nl/",
    "https://www.hellofresh.ie/",
    "https://www.hersheyland.com/",
    "https://www.homechef.com/",
    "https://hostthetoast.com/",
    "https://www.ica.se/",
    "https://receitas.ig.com.br/",
    "https://www.im-worthy.com/",
    "https://indianhealthyrecipes.com",
    "https://www.innit.com/",
    "https://insanelygoodrecipes.com",
    "https://inspiralized.com/",
    "https://izzycooking.com/",
    "https://jamieoliver.com/",
    "https://jimcooksfoodgood.com/",
    "https://joyfoodsunshine.com/",
    "https://juliegoodwin.com.au/",
    "https://justataste.com/",
    "https://justbento.com/",
    "https://www.justonecookbook.com/",
    "https://kennymcgovern.com/",
    "https://www.kingarthurbaking.com",
    "https://www.kitchenstories.com/",
    "https://kochbar.de/",
    "https://kochbucher.com/",
    "http://koket.se/",
    "https://www.kptncook.com/",
    "https://kuchnia-domowa.pl/",
    "https://www.kwestiasmaku.com/",
    "https://www.latelierderoxane.com",
    "https://leanandgreenrecipes.net",
    "https://lecremedelacrumb.com/",
    "https://www.lecker.de",
    "https://lekkerensimpel.com",
    "https://lifestyleofafoodie.com",
    "https://littlespicejar.com/",
    "http://livelytable.com/",
    "https://lovingitvegan.com/",
    "https://www.maangchi.com",
    "https://madensverden.dk/",
    "https://www.madewithlau.com/",
    "https://madsvin.com/",
    "https://marleyspoon.com.au/",
    "https://marleyspoon.com/",
    "https://marleyspoon.de/",
    "https://marleyspoon.at/",
    "https://marleyspoon.be/",
    "https://marleyspoon.nl/",
    "https://marleyspoon.se/",
    "https://marmiton.org/",
    "https://www.marthastewart.com/",
    "https://matprat.no/",
    "https://meljoulwan.com/",
    "https://www.melskitchencafe.com/",
    "http://mindmegette.hu/",
    "https://minimalistbaker.com/",
    "https://ministryofcurry.com/",
    "https://misya.info/",
    "https://www.mob.co.uk/",
    "https://momswithcrockpots.com/",
    "https://monsieur-cuisine.com/",
    "http://motherthyme.com/",
    "https://www.mundodereceitasbimby.com.pt/",
    "https://mybakingaddiction.com/",
    "https://mykitchen101.com/",
    "https://mykitchen101en.com/",
    "https://www.myplate.gov/",
    "https://myrecipes.com/",
    "https://healthyeating.nhlbi.nih.gov/",
    "https://nibbledish.com/",
    "https://www.nhs.uk/healthier-families/",
    "https://www.nosalty.hu/",
    "https://nourishedbynutrition.com/",
    "https://www.nrk.no/",
    "https://www.number-2-pencil.com/",
    "https://nutritionbynathalie.com/blog",
    "https://nutritionfacts.org/",
    "https://cooking.nytimes.com/",
    "https://ohsheglows.com/",
    "https://omnivorescookbook.com",
    "https://www.onceuponachef.com",
    "https://owen-han.com/",
    "https://101cookbooks.com/",
    "https://www.paleorunningmomma.com/",
    "https://www.panelinha.com.br/",
    "https://paninihappy.com/",
    "https://www.persnicketyplates.com/",
    "https://pinchofyum.com/",
    "https://www.pickuplimes.com/",
    "https://www.pingodoce.pt/",
    "https://pinkowlkitchen.com/",
    "https://www.platingpixels.com/",
    "https://plowingthroughlife.com/",
    "https://popsugar.com/",
    "https://practicalselfreliance.com/",
    "https://pressureluckcooking.com/",
    "https://www.primaledgehealth.com/",
    "https://www.projectgezond.nl/",
    "https://przepisy.pl/",
    "https://purelypope.com/",
    "https://purplecarrot.com/",
    "https://rachlmansfield.com/",
    "https://rainbowplantlife.com/",
    "https://realfood.tesco.com/",
    "https://realsimple.com/",
    "https://www.receitasnestle.com.br",
    "https://reciperunner.com/",
    "https://recipetineats.com/",
    "https://redhousespice.com/",
    "https://reishunger.de/",
    "https://rezeptwelt.de/",
    "https://ricetta.it/",
    "https://www.ricetteperbimby.it/",
    "https://rosannapansino.com",
    "https://rutgerbakt.nl/",
    "https://www.saboresajinomoto.com.br/",
    "https://sallysbakingaddiction.com",
    "https://sallys-blog.de",
    "https://saltpepperskillet.com/",
    "https://www.saveur.com/",
    "https://seriouseats.com/",
    "https://simple-veganista.com/",
    "https://simplyquinoa.com/",
    "https://simplyrecipes.com/",
    "https://simplywhisked.com/",
    "https://simply-cookit.com/",
    "https://skinnytaste.com/",
    "https://sobors.hu/",
    "https://www.southerncastiron.com/",
    "https://southernliving.com/",
    "https://spendwithpennies.com/",
    "https://www.springlane.de",
    "https://www.staysnatched.com/",
    "https://steamykitchen.com/",
    "https://streetkitchen.hu/",
    "https://sunbasket.com/",
    "https://sundpaabudget.dk/",
    "https://www.sunset.com/",
    "https://sweetcsdesigns.com/",
    "https://sweetpeasandsaffron.com/",
    "https://www.taste.com.au/",
    "https://tasteofhome.com",
    "https://tastesbetterfromscratch.com",
    "https://tastesoflizzyt.com",
    "https://tasty.co",
    "https://tastykitchen.com/",
    "https://theclevercarrot.com/",
    "https://theexpertguides.com/",
    "https://thehappyfoodie.co.uk/",
    "https://www.thekitchenmagpie.com/",
    "https://thekitchencommunity.org/",
    "https://thekitchn.com/",
    "https://www.themagicalslowcooker.com/",
    "https://themodernproper.com/",
    "https://www.thepalatablelife.com",
    "https://thepioneerwoman.com/",
    "https://therecipecritic.com/",
    "https://thespruceeats.com/",
    "https://thevintagemixer.com/",
    "https://thewoksoflife.com/",
    "https://thinlicious.com/",
    "https://timesofindia.com/",
    "https://tine.no/",
    "https://tidymom.net",
    "https://tudogostoso.com.br/",
    "https://twopeasandtheirpod.com/",
    "https://uitpaulineskeuken.nl/",
    "https://usapears.org/",
    "https://www.valdemarsro.dk/",
    "https://vanillaandbean.com/",
    "https://www.vegetarbloggen.no/",
    "https://vegolosi.it/",
    "https://vegrecipesofindia.com/",
    "https://www.waitrose.com/",
    "https://watchwhatueat.com/",
    "https://wearenotmartha.com/",
    "https://www.weightwatchers.com/",
    "https://www.wellplated.com/",
    "https://whatsgabycooking.com/",
    "https://www.wholefoodsmarket.com/",
    "https://www.wholefoodsmarket.co.uk/",
    "https://www.williams-sonoma.com/",
    "https://woop.co.nz/",
    "https://woolworths.com.au/shop/recipes",
    "https://en.wikibooks.org/",
    "https://yemek.com/",
    "https://yummly.com/",
    "https://www.zaubertopf.de",
    "https://zeit.de/",
    "https://zenbelly.com/",
]


recipe_websites = [
    # "https://www.bbcgoodfood.com/",
    "https://www.epicurious.com/",
    "https://cooking.nytimes.com/",

    "https://www.allrecipes.com/",
    "https://www.foodnetwork.com/",
    "https://www.simplyrecipes.com/",
    "https://www.food.com/",
    "https://www.bettycrocker.com/",
    "https://www.bonappetit.com/",

    # "https://www.tasteofhome.com/",
    # "https://www.myrecipes.com/",
    # "https://www.delish.com/",
]


def recipe_urls():

    def is_recipe_url(soup) -> bool:

        for schema_data in get_schema_data(soup):
            schema_type = schema_data.get("@type", "nope")
            if schema_type == "Recipe":
                return True
        return False

    def get_sitemap_urls(recipe_website):
        recipe_website = recipe_website.rstrip("/")
        pwd = os.path.dirname(os.path.realpath(__file__))
        slug_url = recipe_website.replace("https://", "").replace("http://", "").replace("/", "_").rstrip("/")
        filepath = os.path.join(pwd, f"../../cache/sitemaps/{slug_url}.sitemap.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)

        print("getting sitemap for: ", recipe_website)
        try:

            from usp.tree import sitemap_tree_for_homepage

            tree = sitemap_tree_for_homepage(recipe_website)
            sitemap = tree.all_pages()
            sitemap = [page.url for page in sitemap]
        except Exception:
            print("error getting sitemap for: ", recipe_website)
            return []
        if len(sitemap) == 0:
            return []

        dir = os.path.dirname(filepath)
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(filepath, "w") as f:
            json.dump(sitemap, f)
        return sitemap

    sitemap_urls = {}
    sitemap_urls_indices = {}
    for recipe_website in recipe_websites:
        urls = list(get_sitemap_urls(recipe_website))
        urls = [url for url in urls if "recipes/" in url]
        sitemap_urls[recipe_website] = urls
        sitemap_urls_indices[recipe_website] = 0

    def _interleaved_urls():
        while True:
            for recipe_website in recipe_websites:
                urls = sitemap_urls[recipe_website]
                index = sitemap_urls_indices[recipe_website]
                if index >= len(urls):
                    continue
                sitemap_urls_indices[recipe_website] += 1
                yield urls[index], index, len(urls)

    for url, index, total in _interleaved_urls():
        content = get_cached(url)
        if content is None:
            continue
        if is_recipe_url(BeautifulSoup(content, "html.parser")):
            yield url, index, total


if __name__ == "__main__":
    async def walk():
        generator = recipe_urls()
        async for url_coroutine in generator:
            url = url_coroutine
            print(url)

    asyncio.run(walk())
