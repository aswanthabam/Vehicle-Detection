import styles from "./About.module.css";

export const About = () => {
  return (
    <div className={styles.about}>
      <h1>About</h1>
      <p>
        This is a simple web application that detects vehicles in an image using
        a pre-trained model. The model is based on the YOLO (You Only Look Once)
        architecture, which is a popular object detection algorithm. The model
        is trained on the COCO dataset, which contains 80 different classes of
        objects. The model is able to detect vehicles with high precision and
        accuracy, making it suitable for a wide range of applications, such as
        traffic monitoring, parking management, and security surveillance.
      </p>
      <div className={styles.flexFull}>
        <div className={styles.features}>
          <h2>Features</h2>
          <ul>
            <li>Upload an image and detect vehicles in it</li>
            <li>View the detected vehicles and their bounding boxes</li>
            <li>View the counts of each type of vehicles</li>
            <li>Simple and easy to use designs.</li>
            <li>Fast and effective processing with flask.</li>
          </ul>
        </div>
        <div className={styles.technologies}>
          <h2>Technologies</h2>
          <ul>
            <li>React JS</li>
            <li>Vite JS</li>
            <li>TypeScript</li>
            <li>Flask</li>
            <li>YOLO V3</li>
          </ul>
        </div>
      </div>
        
    </div>
  );
};
