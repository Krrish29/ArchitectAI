import { useContext } from "react";
import { BlueprintContext } from "../context/BlueprintContext";

const useBlueprint = () => {
  return useContext(BlueprintContext);
};

export default useBlueprint;