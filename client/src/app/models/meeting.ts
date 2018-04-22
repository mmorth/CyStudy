/**
 * Represents a study group meeting.
 */
export class Meeting {
  constructor(
    /**
     * The location of the meeting.
     */
    public location: any = "",

    /**
     * The latitude of the meeting.
     */
    public lat: number = 42.026619,

    /**
     * The longitude of the meeting.
     */
    public lng: number = -93.646465,

    /**
     * The date of the meeting.
     */
    public date: string = "",

    /**
     * The time of the meeting.
     */
    public time: string = "",

    /**
     * A description of the meeting.
     */
    public description: string = ""
  ) {}
}
