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

Each separate file contains details of a single 'Service', and so
contains a single Service element, but then stands alone containing
copies of all other referenced entities (which may therefore be repeated
between files). Because files contain a single Service they also contain
a single Operator.

Each Service element contains a single Line element. Most LinesNames
appear associates with a single Service, but occasionally appear in more
than one. This is associated with different Service
OperatingPeriods and presumably represents scheduled timetable changes
for that Line. The final component of the ServiceCode which is identical
to the id attribute of the Line entity and which forms the corresponding
XML filename seems to be a generation number which is incremented when
this happens.

The OperatingPeriod for most services in any one EA.zip file seems to be
identical (from 2017-10-10 to 2018-04-13 for a copy of the file
extracted on 2017-10-23). When this isn't the case it seems to be
associated with scheduled timetable changes (see above) or what could
well be new services being introduced or old ones withdrawn.

OperatingProfile elements are associated with Services and
VehicleJournies, but there are no current examples of them being
associated with JopurneyPatterns (though this is allowed by the schema).

Term-time/Holiday variants seem to be handled by one or both of

* A note associated with relevant VehicleJourneys, normally with
  NoteCode SchO and SchC
* Explicit DaysOfNonOperation (never, apparently, DaysOfOperation)

In practice a common (perhaps only) use of the <HolidaysOnly> 
RegularDaysType is for constructs like this:

```<OperatingProfile>
        <RegularDayType>
          <HolidaysOnly />
        </RegularDayType>
        <BankHolidayOperation>
          <DaysOfOperation>
            <EasterMonday />
          </DaysOfOperation>
          <DaysOfNonOperation />
        </BankHolidayOperation>
      </OperatingProfile>```

The files implement a 1:1 relationship between
JourneyPatterns and JourneyPatternSections, and between Routes and
RouteSections.

Very few VehicleJourneys include VehicleJourneyTimingLinks, implying
that the VehicleJourney keeps to the JourneyPatternTimingLinks of the
underlying JourneyPattern. Where VehicleJourneyTimingLinks appear, they
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

```
TransXChange @Modification @SchemaVersion @schemaLocation @RegistrationDocument
          @FileName @ModificationDateTime @RevisionNumber @CreationDateTime
    StopPoints
        AnnotatedStopPointRef
            StopPointRef
            CommonName
            Indicator
            LocalityName
            LocalityQualifier
    RouteSections
        RouteSection @id
            RouteLink @id
                From
                    StopPointRef
                To
                    StopPointRef
                Direction
    Routes
        Route @id
            PrivateCode
            Description
            RouteSectionRef
    JourneyPatternSections
        JourneyPatternSection @id
            JourneyPatternTimingLink @id
                From @SequenceNumber
                    Activity
                    StopPointRef
                    TimingStatus
                To @SequenceNumber
                    Activity
                    StopPointRef
                    TimingStatus
                    WaitTime
                RouteLinkRef
                RunTime
    Operators
        Operator @id
            NationalOperatorCode
            OperatorCode
            OperatorShortName
            OperatorNameOnLicence
            TradingName
            LicenceNumber
            LicenceClassification
    Services
        Service
            ServiceCode
            PrivateCode
            Lines
                Line @id
                    LineName
            OperatingPeriod
                StartDate
                EndDate
            OperatingProfile
                RegularDayType
                    DaysOfWeek
                        MondayToSunday
                        Monday
                        Wednesday
                        Thursday
                        Friday
                        Saturday
                        MondayToFriday
                        MondayToSaturday
                        Sunday
                        Tuesday
                        Weekend
                SpecialDaysOperation
                    DaysOfNonOperation
                        DateRange
                            StartDate
                            EndDate
                BankHolidayOperation
                    DaysOfNonOperation
                        ChristmasDay
                        BoxingDay
                        GoodFriday
                        NewYearsDay
                        EasterMonday
                        AllBankHolidays
            RegisteredOperatorRef
            StopRequirements
                NoNewStopsRequired
            Mode
            Description
            StandardService
                Origin
                Destination
                JourneyPattern @id
                    Direction
                    RouteRef
                    JourneyPatternSectionRefs
                    Operational
                        VehicleType
                            VehicleTypeCode
                            Description
    VehicleJourneys
        VehicleJourney
            PrivateCode
            OperatingProfile
                RegularDayType
                    DaysOfWeek
                        MondayToFriday
                        Saturday
                        Sunday
                        Wednesday
                        Thursday
                        Friday
                        Monday
                        Tuesday
                    HolidaysOnly
                SpecialDaysOperation
                    DaysOfNonOperation
                        DateRange
                            StartDate
                            EndDate
                BankHolidayOperation
                    DaysOfNonOperation
                        ChristmasDay
                        BoxingDay
                        GoodFriday
                        NewYearsDay
                        EasterMonday
                        AllBankHolidays
                    DaysOfOperation
                        EasterMonday
                        GoodFriday
                        BoxingDay
            VehicleJourneyCode
            ServiceRef
            LineRef
            JourneyPatternRef
            DepartureTime
            Note
                NoteCode
                NoteText
            Operational
                VehicleType
                    VehicleTypeCode
                    Description
            VehicleJourneyTimingLink @id
                JourneyPatternTimingLinkRef
                From
                To
```