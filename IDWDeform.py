        ### <Summary>
        ### Calculates the displacements of the volume points
        ### using the displacements of each surface point.
        ### Currently doesn't enforce that farfield stays fixed.
        ### </Summary>
        ### <Returns>
        ### A vector of CFD displacements as a numpy array.
        ### </Returns>
        def IDWDeform(self):
                np.seterr(divide="raise")
                xyz = self.GetMeshUndeformedCoordinates()
                dxyzSurf = self.GetDisplacements()
                dxyzVol = np.zeros(xyz.shape)

                for i in range(xyz.shape[0]):
                        try:
                                weights = xyz[i] - self.basePoints
                                weights = np.linalg.norm(weights, axis=1) ** (-2)
                        except:
                                # Catch the div0 if the current volume point is
                                # also a surface point.
                                weights = np.sum(weights, axis=1)
                                surfInd = np.where(0.0 == weights)[0]
                                weights = np.zeros(len(weights))
                                weights[surfInd] = 1.0

                        weightSum = np.sum(weights)
                        weights = weights/weightSum
                        dxyzVol[i,0] = np.dot(weights, dxyzSurf[:,0])
                        dxyzVol[i,1] = np.dot(weights, dxyzSurf[:,1])
                        dxyzVol[i,2] = np.dot(weights, dxyzSurf[:,2])
		
                return dxyzVol
