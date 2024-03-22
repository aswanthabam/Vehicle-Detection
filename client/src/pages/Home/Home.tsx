import styles from "./Home.module.css";
import { useState } from "react";
import { ProcessResponse } from "../../types";
import { processImage } from "../../api/proccessApi";

export const Home = () => {
  const [response, setResponse] = useState<ProcessResponse | null>();
  const [uploadPage, setUploadPage] = useState<boolean>(true);
  const processFile = async (file: File) => {
    var res = await processImage(file);
    setResponse(res);
    setUploadPage(!res.status);
  };
  return (
    <div className={styles.home}>
      <h1>Vehicle Detection</h1>
      {uploadPage ? (
        <>
          <div
            className={styles.dropZone}
            onDragOver={(e) => {
              e.preventDefault();
            }}
            onDrop={async (e) => {
              e.preventDefault();
              var files = e.dataTransfer.files;
              var file = files[0];
              processFile(file);
            }}
          >
            <p>
              Drag one or more files to this <i>drop zone</i>.
            </p>
          </div>
        </>
      ) : (
        <div className={styles.buttonContainer}>
          <button
            className={styles.uploadButton}
            onClick={() => {
              setUploadPage(true);
              setResponse(null);
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              className="bi bi-arrow-repeat"
              viewBox="0 0 16 16"
            >
              <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9" />
              <path
                fillRule="evenodd"
                d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"
              />
            </svg>
            Upload Another Image
          </button>
        </div>
      )}
      {response &&
        (response.status && response.data ? (
          <>
            <div className={styles.resultImages}>
              <img src={response.data.upload_url} alt="result" />
              <img src={response.data.result_url} alt="uploaded" />
            </div>
            <div className={styles.resultData}>
              <h2>Vehicle Counts</h2>
              <div className={styles.result}>
                <div className={styles.head + " " + styles.row}>
                  <div className={styles.cell}>Vehicle</div>
                  <div className={styles.cell}>Count</div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Bicycle</div>
                  <div className={styles.cell}>
                    {response.data.result.bicycle}
                  </div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Car</div>
                  <div className={styles.cell}>{response.data.result.car}</div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Bus</div>
                  <div className={styles.cell}>{response.data.result.bus}</div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Motorbike</div>
                  <div className={styles.cell}>
                    {response.data.result.motorbike}
                  </div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Person</div>
                  <div className={styles.cell}>
                    {response.data.result.person}
                  </div>
                </div>
                <div className={styles.row}>
                  <div className={styles.cell}>Truck</div>
                  <div className={styles.cell}>
                    {response.data.result.truck}
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div>
            <h2>Error</h2>
            <p>{response.message}</p>
          </div>
        ))}
    </div>
  );
};
