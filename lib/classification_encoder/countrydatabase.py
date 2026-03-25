##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##

import os
import sys
from enum import Enum
from json import loads as json_loads
from typing import List, Optional, Dict

'''
The CountryDatabase class provides a simple interface to access country codes and 
related information. It loads country data from a JSON file and provides lists of 
countries, NATO members, Five Eyes members, Nine Eyes members, and Fourteen Eyes members.
'''
class CountryDatabase:
    def __init__(self):
        """
        Initialize the CountryDatabase.
        
        Loads country data from world.json and initializes alliance lists.
        """
        self.countries3: List[str] = []
        self.countries2: List[str] = []
        self.rawdata: List[Dict] = []
        
        ccodesfile = os.path.join(os.path.dirname(__file__), "world.json")
        with open(ccodesfile, "r", encoding="utf-8", errors="ignore") as f:
            self.rawdata = json_loads(f.read())
            
        for entry in self.rawdata:
            self.countries3.append(entry['alpha3'].upper())
            self.countries2.append(entry['alpha2'].upper())
            
        # NATO member countries (ISO 3166-1 alpha-3 codes)
        self.nato = [
            'ALB', 'BEL', 'BGR', 'CAN', 'HRV', 'CZE', 'DNK', 'EST', 'FIN', 
            'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'ITA', 'LVA', 'LTU', 
            'LUX', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'SVK', 
            'SVN', 'ESP', 'SWE', 'CHE', 'TUR', "GBR", "USA"
        ]
        
        # Five Eyes intelligence alliance
        self.fvey = ["AUS", "CAN", "NZL", "GBR", "USA"]
        
        # Nine Eyes intelligence alliance (FVEY + 4)
        self.nineEyes = ["AUS", "CAN", "NZL", "GBR", "USA", "DNK", "FRA", "NLD", "NOR"]
        
        # Fourteen Eyes intelligence alliance (Nine Eyes + 5)
        self.fourteenEyes = ["AUS", "CAN", "NZL", "GBR", "USA", "DNK", "FRA", "NLD", 
                            "NOR", "BEL", "DEU", "ITA", "ESP", "SWE"]   

    def getAlpha3ForAlpha2(self, alpha2: str) -> Optional[str]:
        """
        Convert ISO 3166-1 alpha-2 code to alpha-3 code.
        
        Args:
            alpha2: Two-letter country code (e.g., "US")
            
        Returns:
            Three-letter country code (e.g., "USA") or None if not found
        """
        for entry in self.rawdata:
            if entry['alpha2'].upper() == alpha2.upper():
                return entry['alpha3'].upper()
        return None

    def parseAndValidateRelto(self, reltoStr: str) -> List[str]:
        """
        Parse and validate a RELTO string, extracting valid country codes.
        
        Takes a REL TO ... line and returns the country codes as a list. 
        Invalid codes are discarded. Alpha-2 codes are normalized to alpha-3.
        
        Args:
            reltoStr: RELTO string like "REL TO USA, GBR, CAN" or "USA, GBR, CAN"
            
        Returns:
            List of valid ISO 3166-1 alpha-3 country codes
            
        Example:
            >>> db = CountryDatabase()
            >>> db.parseAndValidateRelto("REL TO US, GB, CA")
            ['USA', 'GBR', 'CAN']
        """
        if reltoStr.startswith("REL TO"):
            reltoStr = reltoStr[len("REL TO"):]
            
        CCODES = []
        for CX in reltoStr.split(","):
            CX = CX.strip()
            if len(CX) == 2:
                # If we find it, normalize it to alpha-3 which is what they're supposed
                # to be using
                if CX.upper() in self.countries2:
                    CX2 = self.getAlpha3ForAlpha2(CX)
                    if CX2 is not None:
                        CCODES.append(CX2)
            elif len(CX) == 3:
                if CX.upper() in self.countries3:
                    CCODES.append(CX.upper())
        return CCODES

    def isNATO(self, countryList: List[str]) -> bool:
        """
        Check if a country list exactly matches NATO members.
        
        Args:
            countryList: List of ISO 3166-1 alpha-3 country codes
            
        Returns:
            True if the list exactly matches NATO membership
        """
        return set(self.nato) == set(countryList)

    def isFVEY(self, countryList: List[str]) -> bool:
        """
        Check if a country list exactly matches Five Eyes members.
        
        Args:
            countryList: List of ISO 3166-1 alpha-3 country codes
            
        Returns:
            True if the list exactly matches Five Eyes membership
        """
        return set(self.fvey) == set(countryList)

    def isNineEyes(self, countryList: List[str]) -> bool:
        """
        Check if a country list exactly matches Nine Eyes members.
        
        Args:
            countryList: List of ISO 3166-1 alpha-3 country codes
            
        Returns:
            True if the list exactly matches Nine Eyes membership
        """
        return set(self.nineEyes) == set(countryList)

    def isFourteenEyes(self, countryList: List[str]) -> bool:
        """
        Check if a country list exactly matches Fourteen Eyes members.
        
        Args:
            countryList: List of ISO 3166-1 alpha-3 country codes
            
        Returns:
            True if the list exactly matches Fourteen Eyes membership
        """
        return set(self.fourteenEyes) == set(countryList)

##
## UNCLASSIFIED
## Classification markings are for code purposes only and do not indicate 
## classification.
##
