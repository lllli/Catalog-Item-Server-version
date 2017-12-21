from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import base, Platform, Game, User

engine = create_engine('postgresql://catalog:password@localhost/catalog')
base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()

session.query(Platform).delete()
session.query(Game).delete()
platforms = ['PlayStation','Xbox','Nintendo Switch','PC']
#for platform in platforms:
#    cata = Platform(name=platform)
#    session.add(cata)
#    session.commit()
platform1 = Platform(name='PlayStation')
session.add(platform1)
#session.commit
platform2 = Platform(name='Xbox')
session.add(platform2)
#session.commit
platform3 = Platform(name='Nintendo Switch')
session.add(platform3)
#session.commit
platform4 = Platform(name='PC')
session.add(platform4)
session.commit


item1 = Game(title="Horizon Zero Dawn - Complete Edition",
             description="Horizon Zero Dawn is an exhilarating action role playing game exclusively for the PlayStation 4 System, developed by the award winning Guerrilla Games, creators of PlayStation's venerated Killzone franchise. Take on the role of skilled hunter Aloy as you explore a vibrant and lush world inhabited by mysterious mechanized creatures. Embark on a compelling, emotional journey and unravel mysteries of tribal societies, ancient artifacts and advanced technologies that will determine the fate of this planet, and of life itself.",
             cover="https://images-na.ssl-images-amazon.com/images/I/91qUDrHSkLL._AC_SL1500_.jpg",
             release="December 5, 2017",
             platform_id=platform1.id)
session.add(item1)
session.commit()


item2 = Game(title="Assassin's Creed Origins",
             description="Ancient Egypt & dash : home of colossal pyramids, gilded tombs, tyrannical god-kings, and the origin story of the Assassins. As Cleopatra empire crumbles, the birth of the Assassin's Brotherhood will lead to an extraordinary shift of the world order. Along your journey, the mysteries of Ancient Egypt will be revealed. Assassin Creed Origins uncovers the beginning of the Brotherhood. Fight in epic battles, master a completely reinvented combat system, and explore the entirety of Egypt. With the all-new quest system, complete missions in any order you choose, and follow your own path to greatness.",
             cover="https://images-na.ssl-images-amazon.com/images/I/91HjQ2QdjLL._AC_SL1500_.jpg",
             release="October 27, 2017",
             platform_id=platform1.id)
session.add(item2)
session.commit()


item3 = Game(title="Star Wars Battlefront II",
             description="Rush through waves of enemies of Starkiller Base with the power of your lightsaber in your hands. Store through the jungle canopy of a hidden Rebel base on Yavin 4 with your fellow troopers, dispensing firepower from AT-STs. Line up your X-wing squadron for an attact on a mammoth First Order Star Destroyer in space. Or rise as a new Star Wars hero - Iden, an elite Imperial special forces soldier - and discover an emothional and gripping single-player story spanning thirty years.",
             cover="https://images-na.ssl-images-amazon.com/images/I/71an0z4csGL._AC_SL1000_.jpg",
             release="November 17, 2017",
             platform_id=platform1.id)
session.add(item3)
session.commit()


item4 = Game(title="Call of Duty: WWII",
             description="Call of Duty returns to its roots with Call of Duty: WWII-a breathtaking experience that redefines World War II for a new gaming generation. Land in Normandy on D-Day and battle across Europe through iconic locations in history's most monumental war. Experience classic Call of Duty combat, the bonds of camaraderie, and the unforgiving nature of war against a global power throwing the world into tyranny",
             cover="https://images-na.ssl-images-amazon.com/images/I/91uIuoa85PL._AC_SL1500_.jpg",
             release="November 3, 2017",
             platform_id=platform1.id)
session.add(item4)
session.commit()


item5 = Game(title="Halo 5: Guardians",
             description="An intense new story on a galactic scale: Play as the Master Chief and Spartan Locke as the hunt plays out across three new worlds. Your team is your weapon: Choose how to achieve objectives while playing solo with AI teammates or with friends in a 4-player cooperative experience using your Xbox Live 14-day Gold trial.",
             cover="https://images-na.ssl-images-amazon.com/images/I/71jUlLTTl3L._AC_SL1380_.jpg",
             release="October 27, 2015",
             platform_id=platform2.id)
session.add(item5)
session.commit()

item6 = Game(title="Forza Motorsport 7",
             description="The ULTIMATE RACING EXPERIENCE. BUILT FOR 4K. The best-selling racing franchise on any platform this generation. Experience the thrill of motorsport at the limit with the most comprehensive, beautiful and authentic racing game ever made. ENjoy gorgeous graphics at 60fps and true 4K resolution in HDR. Collect and race more than 700 cars. Challenge yourself across 30 famous destinations 200 ribbons, where race conditions can change every lap and every race.",
             cover="https://images-na.ssl-images-amazon.com/images/I/71A261zl%2BcL._AC_SL1200_.jpg",
             release="October 3, 2017",
             platform_id=platform2.id)
session.add(item6)
session.commit()

item7 = Game(title="The Legend of Zelda: Breath of the Wild",
             description="Step into a world of discovery, exploration, and adventure in The Legend of Zelda: Breath of the Wild, a boundary-breaking new game in the acclaimed series. Travel across vast fields, through forests, and to mountain peaks as you discover what has become of the kingdom of Hyrule in this stunning Open-Air Adventure. Now on the Nintendo Switch console, your journey is freer and more open than ever. Take your system anywhere, and adventure as Link any way you like.",
             cover="https://images-na.ssl-images-amazon.com/images/I/71y3rzfuUlL._AC_SL1000_.jpg",
             release="March 3, 2017",
             platform_id=platform3.id)
session.add(item7)
session.commit()

item8 = Game(title="Super Mario Odyssey",
             description="Explore huge 3D kingdoms filled with secrets and surprises, including costumes for Mario and lots of ways to interact with the diverse environments - such as cruising around them in vehicles that incorporate the HD Rumble feature of the Joy-Con controller or exploring sections as Pixel Mario. Thanks to his new friend, Cappy, Mario has brand-new moves for you to master, like cap throw, cap jump and capture. With capture, Mario can take ontrol of all sorts of things, including objects and enemies!",
             cover="https://images-na.ssl-images-amazon.com/images/I/91SF0Tzmv4L._AC_SL1500_.jpg",
             release="October 27, 2017",
             platform_id=platform3.id)
session.add(item8)
session.commit()

item9 = Game(title="World of Warcraft",
             description="Descend into the World of Warcraft and join thousands of mighty heroes in an online world of myth, magic, and limitless adventure. Explore jagged, snowy peaks; vast mountain fortresses; and harsh, winding canyons. Witness zeppelins flying over smoldering battlefields; battle inepic sieges - a host of legendary experiences await. Enter the World of Warcraft...",
             cover="https://images-na.ssl-images-amazon.com/images/I/91g59vHdaGL._AC_SL1500_.jpg",
             release="October 14, 2013",
             platform_id=platform4.id)
session.add(item9)
session.commit()

item10 = Game(title="Sid Meier's Civilization VI",
             description="Originally created by legendary game designer Sid Meier, Civilization is a turn-based strategy game in which you attempt to build an empire to stand the test of time. Become Ruler of the World by establishing and leading a civilization from the Stone Age to the information Age. Wage war, conduct diplomacy, advance your culture, and go head-to-head with history's greatest leaders as you attempt to build the greatest civilization the world has ever known.",
             cover="https://images-na.ssl-images-amazon.com/images/I/D1dwJgXivgS.jpg",
             release="October 20, 2016",
             platform_id=platform4.id)
session.add(item10)
session.commit()
