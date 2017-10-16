Travelline TNDS timetable data
==============================

Timetable data from

    ftp://ftp.tnds.basemap.co.uk/EA.zip

(registration required). See

    ftp://ftp.tnds.basemap.co.uk/servicereport.csv

for a list of content and what components of the filenames mean. The
file

    ftp://ftp.tnds.basemap.co.uk/log.txt

is vaguely amusing.

The data is in TransXChange 2.1 format (current is 2.5):

    xsi:schemaLocation="http://www.transxchange.org.uk/ http://www.transxchange.org.uk/schema/2.1/TransXChange_general.xsd"

    http://www.transxchange.org.uk/schema/2.1/TransXChange_general.xsd
    http://naptan.dft.gov.uk/transxchange/schema/2.1/TransXChange_common.xsd

    http://naptan.dft.gov.uk/transxchange/

Universal service data in `EA/ea_20-U-_-y08-1.xml`

Likewise CITI7 date in `EA/ea_20-7-A-y08-1.xml`

TransXChangePublisher (currently 2.4_5) looks interesting, but doesn't seem to work on Unix

Observed features of the TNDS data
----------------------------------

Each separate file appears to represent a 'line', containing a single
Service entity itself containing a single Line entity, but then stands
alone containing copies of all other referenced entities. Because files
contain a single Service they also contain a single Operator.

The files implement a 1:1 relationship between
JourneyPatterns and JourneyPatternSections, and between Routes and
RouteSections. 

Very few VehicleJourneys include VehicleJourneyTimingLinks, implying
that the VehicleJourney keeps to the JourneyPatternTimingLinks of the
underlying JourneyPattern. Where VehicleJourneyTimingLinks apepar, they
only contain empty To and From entities.

SequenceNo
----------

SequenceNo is an attribute of the From and To entities in a
JourneyPatternTimingLink. It provides a sort key (unique for any given
Service and JourneyPattern Direction) for ordering the timing
information for the corresponding stop in a matrix timetable.

Direction is part of the uniqueness constraint because many stops
are common to inbound and outbound trips (especially those at either
end) but need to appear in different places in the timetable.

SequenceNo is not an attribute of a stop. That's because some stops
appear more then once in a journey (typically with separate
arrival/departure times) such as at the Railway Station on the
Universal. However in the entire EA.zip file there are no examples of
the same Service/Direction/SerialNo appearing with more than one
StopPointRef. Further there are no To or From entities in the entire
EA.zip file that don't include a SequenceNo attribute (though it is
optional according to schema).

Observed TransXChange structure
-------------------------------

[See also TNDS_ERD.dia]

- TransXChange[CreationDateTime,ModificationDateTime,Modification,
  RevisionNumber,FileName,SchemaVersion,RegistrationDocument]
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
