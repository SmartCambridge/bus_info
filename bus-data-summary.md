Timetable data from 

    ftp://amc203@cam.ac.uk:6t9W.wdCHHpDVu3HyQd)@ftp.tnds.basemap.co.uk/EA.zip

It's in TransXChange format:

    xsi:schemaLocation="http://www.transxchange.org.uk/ http://www.transxchange.org.uk/schema/2.1/TransXChange_general.xsd"

    http://naptan.dft.gov.uk/transxchange/

Universal service data in `EA/ea_20-U-_-y08-1.xml`

Likewise CITI7 date in `EA/ea_20-7-A-y08-1.xml`

This seems to be in schema version 2.1. Current is 2.5

TransXChangePublisher (currently 2.4_5) looks interesting, but doesn't seem to work on Unix

Observed TransXChange format:

- TransXChange[CreationDateTime,ModificationDateTime,Modification,RevisionNumber,FileName,SchemaVersion,RegistrationDocument]
    - StopPoints
        - AnnotatedStopPointRef +
            - **StopPointRef**
            - Common Name
            - Indicator
            - LocalityName
            - LocalityQualifier
    - RouteSections
        - RouteSection[**id**] +
            - RouteLink[**id**] +
                - From
                    - *StopPointRef*
                - To
                    - *StopPointRef*
                - Direction
    - Routes
        - Route[**id**] +
            - PrivateCode
            - Description
            - *RouteSectionRef*
    - JourneyPatternSections
        - JourneyPatternSection[**id**] +
            - JourneyPatternTimingLink[id] +
                - From[SequenceNumber]
                    - Activity
                    - *StopPointRef*
                    - TimingStatus
                - To[SequenceNumber]
                    - Activity
                    - *StopPointRef*
                    - TimingStatus
                - *RouteLinkRef*
                - RunTime
    - Operators
        - Operator[**id**] +
            - NationalOperatorCode
            - OperatorCode
            - OperatorShortName
            - OperatorNameOnLicence
            - TradingAs
    - Services
        - Service +
            - **ServiceCode**
            - PrivateCode
            - Lines
                - Line[**id**] +
                    - LineName
            - OperatingPeriod
                - StartDate
                - EndDate
            - OperatingProfile
                - RegularDayType
                    - DaysOfWeek
                        - _[whatever]_ +
            - _RegisteredOperatorRef_
            - StopRequirements
                - _[whatever]_ +
            - Mode
            - Description
            - StandardService
                - Origin
                - Destination
                - JourneyPattern[**id**] +
                    - Direction
                    - *RouteRef*
                    - *JourneypatternSectionRef*
    - VehicleJourneys
        - VehicleJourney +
            - PrivateCode
            - OperatingProfile
                - RegularDayType
                    - DaysofWeek
                        - _[whatever]_ +
                - SpecialDaysOperation
                    - DaysOfNotOperation +
                        - DateRange
                            - StartDate
                            - EndDAte
                - BankHolidayOperation
                    - DaysOfNonOperation
                        - _[whatever]_ +
            - VehicleJourneyCode
            - *ServiceRef*
            - *LineRef*
            - *JourneyPatternRef*
            - DepartureTime

Features of the TNDS data:

* One service per file (implies one operator per file)
* One line per service
* One route section per route
* One JourneyPatternSection per JourneyPattern