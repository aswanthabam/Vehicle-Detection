import styles from "./Home.module.css";
import { useRef, useState } from "react";
import { ProcessResponse } from "../../types";
import { processImage } from "../../api/proccessApi";
import loadingGif from "../../assets/loading.gif";

export const Home = () => {
  const [response, setResponse] = useState<ProcessResponse | null>();
  const uploadRef = useRef<HTMLDivElement>(null);
  const resultRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);

  const processFile = async (file: File) => {
    setLoading(true);
    var res = await processImage(file);
    setResponse(res);
    setLoading(false);
    new Promise((resolve) => {
      setTimeout(() => {
        resolve(true);
      }, 100);
    }).then(() => {
      resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
    });
  };
  return (
    <div className={styles.home}>
      <div id={styles.upload} ref={uploadRef}>
        <div className={styles.introduction}>
          <h1>Vehicle Detection</h1>
          <p>
            In today's fast-paced world, effective traffic management is
            essential for ensuring the safety and efficiency of our roadways.
            With the advent of advanced technology, automated solutions have
            become increasingly prevalent in addressing these challenges. Our
            Vehicle Detection Project aims to contribute to this effort by
            harnessing the power of computer vision and machine learning to
            detect vehicles in images with precision and accuracy.
          </p>
        </div>
        <div className={styles.mainUpload}>
          {loading ? (
            <div className={styles.loading}>
              <img src={loadingGif} />
              <span>Your image is processing ...</span>
            </div>
          ) : (
            <div
              className={styles.dropZone}
              onClick={() => {
                document.getElementById("fileInput")?.click();
              }}
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                className="bi bi-card-image"
                viewBox="0 0 16 16"
              >
                <path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0" />
                <path d="M1.5 2A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2zm13 1a.5.5 0 0 1 .5.5v6l-3.775-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12v.54L1 12.5v-9a.5.5 0 0 1 .5-.5z" />
              </svg>
              <p>Drag image file or click here to upload.</p>
              <div> Supported formats arejpg, png, webp, bmp, img.</div>
            </div>
          )}
        </div>
      </div>
      {response &&
        (response.status && response.data ? (
          <div ref={resultRef}>
            <div className={styles.buttonContainer}>
              <button
                className={styles.uploadButton}
                onClick={() => {
                  uploadRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
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
            <div className={styles.resultImages}>
              <div className={styles.resultImageContainer}>
                <h2>Original</h2>
              <img src={response.data.upload_url} alt="result" />
              </div>
              <div className={styles.resultImageContainer}>
                <h2>Detected</h2>
              <img src={response.data.result_url} alt="uploaded" />
              </div>
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
          </div>
        ) : (
          <div>
            <h2>Error</h2>
            <p>{response.message}</p>
          </div>
        ))}
      <input
        type="file"
        id="fileInput"
        style={{ display: "none" }}
        onChange={async (e) => {
          var files = e.target.files;
          var file = files ? files[0] : null;
          if (file) {
            processFile(file);
          }
        }}
      />
    </div>
  );
};
