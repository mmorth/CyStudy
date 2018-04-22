/**
 * Interface for a study group.
 */
export interface StudyGroup {
  /**
   * The ID of the study group.
   */
  id: number;

  /**
   * The department of the course for the study group.
   */
  course_department: string;

  /**
   * The number of the course for the study group.
   */
  course_number: number;

  /**
   * The name of the course for the study group.
   */
  course_name: string;

  /**
   * A list of people in the study group.
   */
  members: any[];
}
