import { useEffect, useState } from "react";
import NavBar from "./Navbar/NavBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";

function App() {
  const [uploaded, setUploaded] = useState(false);
  const [loading, setLoading] = useState(false);

  const onSelectImageHandler = (e) => {
    setLoading(true);
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("image", file);

    fetch("http://127.0.0.1:8000/upload/", {
      method: "POST",
      body: formData,
    }).then((data) => {
    });
    setUploaded(true);
  };

  useEffect(() => {
    console.log("chala hai ", uploaded);
    if (uploaded) {
      fetch("http://127.0.0.1:8000/removebg/", {
        method: "GET",
        headers: {
          "Content-Type": "image/jpeg",
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.blob();
          } else {
            throw new Error("Failed to fetch image");
          }
        })
        .then((blob) => {
          const imageUrl = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = imageUrl;
          link.download = "image.jpg";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
      setUploaded(false);
    }
  }, [uploaded]);

  return (
    <>
      <NavBar />
      <Box
        display="flex"
        justifyContent="space-around"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
      >
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          flexDirection="column"
        >
          <Typography
            variant="h4"
            fontWeight="bold"
            align="center"
            sx={{ fontFamily: "monospace" }}
          >
            {" "}
            Upload an image to <br /> remove the background
          </Typography>
          <br />
          <Button variant="contained" component="label">
            {loading ? (
              <CircularProgress style={{ color: "white" }} size={24} />
            ) : (
              <Typography fontWeight="bold">Upload File</Typography>
            )}
            <input type="file" hidden onChange={onSelectImageHandler} />
          </Button>
        </Box>

        {/* <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          flexDirection="column"
          gap={6}
        >
          <Typography fontFamily={"Roboto"}>
            No image? Try one of these:
          </Typography>

          <Grid container spacing={4}>
            <Grid item>
              <img
                style={{ width: "140px" , cursor: "pointer" }}
                src="https://d38b044pevnwc9.cloudfront.net/cutout-nuxt/passport/1-change1.jpg"
              />
            </Grid>
            <Grid item>
              <img
                style={{ width: "140px" }}
                src="https://d38b044pevnwc9.cloudfront.net/cutout-nuxt/passport/1-change1.jpg"
              />
            </Grid>
            <Grid item>
              <img
                style={{ width: "140px" }}
                src="https://d38b044pevnwc9.cloudfront.net/cutout-nuxt/passport/1-change1.jpg"
              />
            </Grid>
          </Grid>
        </Box> */}
      </Box>
    </>
  );
}

export default App;
